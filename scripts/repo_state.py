#!/usr/bin/env python3
"""Print what a katai stage needs to know about the repository it runs in.

A stage runs this script when it loads, with no argument, and reads one
`label: value` line per value. The values come from git, from GitHub through
`gh`, from the repository's plans folder and from the local note. The script
writes nothing, and it prints the text that GitHub returns, such as titles and
branch names, as data that it never runs.

The script runs `git fetch` and each `gh` call side by side, gives each of them
20 seconds and ends within 60, because Claude Code aborts a skill whose
load-time command runs for two minutes. It always exits 0. A value that it
cannot read prints as `<label>: unknown (<reason>)`.

Three cases print one line and nothing else, because a stage stops on them.
The first is no repository, or one whose top level is the home directory. The
second is a main checkout that is a bare repository. The third is an origin
that is not on GitHub.
"""

import concurrent.futures
import datetime
import json
import os
import re
import signal
import subprocess
import sys
import time
from collections import Counter, namedtuple

# The lines a stage stops on. The home directory counts as no repository of
# its own, because a home directory kept in git holds every project below it.
NO_REPOSITORY = "no repository of its own"
BARE_MAIN = "no main checkout (bare)"
NO_GITHUB = "no GitHub origin"

# A network call that takes longer is cut off and its value is unknown.
CALL_SECONDS = 20
# The script must end within 60 seconds. The five seconds left over are for
# the local reads that follow the last network call. They are not measured.
SCRIPT_SECONDS = 55
# A reason longer than this is cut, so that one error does not flood the output.
REASON_CHARS = 120

# git and gh never ask on a terminal, git takes no optional lock (without this
# `git status` may rewrite the index), and gh does not check for an update of
# itself, which would write its state file.
QUIET_ENV = {
    "GIT_TERMINAL_PROMPT": "0",
    "GIT_OPTIONAL_LOCKS": "0",
    "GH_PROMPT_DISABLED": "1",
    "GH_NO_UPDATE_NOTIFIER": "1",
}

GITHUB_PREFIXES = ("git@github.com:", "https://github.com/", "ssh://git@github.com/")
# GitHub's character sets for an account name and for a repository name.
GITHUB_OWNER = re.compile(r"[a-z0-9-]+")
GITHUB_NAME = re.compile(r"[a-z0-9._-]+")

# The windows of history the values are read from.
HISTORY_DAYS = 90
MERGED_SAMPLE = 30
RECENT_COUNT = 5
APPROVAL_SAMPLE = 20
PR_LIST_LIMIT = 200
OPEN_PR_LIMIT = 50
# GitHub's search returns at most 1000 results.
SEARCH_LIMIT = 1000

# An item key of a tracker, such as "ABC-123", in a branch name or a title.
ITEM_KEY = re.compile(r"(?<![A-Za-z0-9])([A-Za-z]{2,})-[0-9]+")

PLAN_KEYS = ("Status", "Item", "Unit", "Branch", "Base")
# A plan's header lines come first in the file, so a key further down is text.
PLAN_HEADER_LINES = 20
CHECK_FILE_SUFFIXES = ("-read-1.md", "-read-2.md", "-audit.md")

NOTE_PATH = os.path.join(".claude", "AGENTS.md")
NOTE_EXCLUDE_LINE = ".claude/AGENTS.md"
RECORD_FOLDER_NAMES = ("adr", "adrs", "decisions")

Checkout = namedtuple("Checkout", "top main common worktrees")
# One entry of `git worktree list`. Its branch is None for a detached head.
Worktree = namedtuple("Worktree", "path branch bare")


# ---------------------------------------------------------------------------
# Parsing and formatting, without git or gh
# ---------------------------------------------------------------------------

def printable(text):
    """Return text with each control character replaced by a space, so data cannot start a line."""
    return "".join(c if c.isprintable() else " " for c in text)


def unknown(label, reason):
    return "%s: unknown (%s)" % (label, reason)


def github_repo(url):
    """Return "owner/repo" of a GitHub address, lowercased, or None for any other address.

    The SSH, HTTPS and ssh:// forms of one repository give the same value, so
    every clone and worktree of it finds the same plans folder.
    """
    lowered = url.strip().lower()
    for prefix in GITHUB_PREFIXES:
        if lowered.startswith(prefix):
            rest = lowered[len(prefix):].rstrip("/")
            rest = rest[:-len(".git")] if rest.endswith(".git") else rest
            owner, _, name = rest.partition("/")
            if GITHUB_OWNER.fullmatch(owner) and GITHUB_NAME.fullmatch(name) \
                    and name not in (".", ".."):
                return owner + "/" + name
    return None


def is_own(login, repo):
    """Return True when the signed-in user is the owner of the repository's GitHub address."""
    return login.lower() == repo.split("/")[0]


def state_dir(home, repo):
    """Return katai's folder for a repository, which lives outside every checkout of it."""
    owner, name = repo.split("/")
    return os.path.join(home, ".local", "state", "katai", "github.com", owner, name)


def plans_dir(home, repo):
    """Return the plans folder of a repository, inside the repository's katai folder."""
    return os.path.join(state_dir(home, repo), "plans")


def same_path(a, b):
    return os.path.realpath(a) == os.path.realpath(b)


def parse_worktrees(text):
    """Return the Worktrees of `git worktree list --porcelain`, the main checkout first."""
    trees = []
    for block in text.strip().split("\n\n"):
        fields = dict(line.partition(" ")[::2] for line in block.splitlines())
        if "worktree" in fields:
            branch = fields.get("branch")
            trees.append(Worktree(fields["worktree"],
                                  branch[len("refs/heads/"):] if branch else None,
                                  "bare" in fields))
    return trees


def format_checkout(top, main):
    if same_path(top, main):
        return "checkout: %s (main)" % top
    return "checkout: %s (linked, main %s)" % (top, main)


def status_counts(porcelain):
    """Return (tracked changes, untracked entries) of `git status --porcelain` output."""
    entries = [line for line in porcelain.splitlines() if line.strip()]
    untracked = sum(1 for line in entries if line.startswith("??"))
    return len(entries) - untracked, untracked


def dig(value, *keys):
    """Return value[k1][k2]... of parsed JSON, or None where a level is missing or null."""
    for k in keys:
        try:
            value = value[k]
        except (KeyError, IndexError, TypeError):
            return None
    return value


def nodes(connection):
    """Return the nodes of a GraphQL connection that are objects."""
    return [n for n in (dig(connection, "nodes") or []) if isinstance(n, dict)]


def merge_style(pr):
    """Return how a merged pull request landed on its base, or None when GitHub names no commit.

    A merge commit has two parents. A base that holds the head commit itself
    took a fast-forward. Any other new commit is a squash, and a rebase merge
    looks the same.
    """
    oid = dig(pr, "mergeCommit", "oid")
    if not oid:
        return None
    if (dig(pr, "mergeCommit", "parents", "totalCount") or 0) > 1:
        return "merge commit"
    if oid == pr.get("headRefOid"):
        return "fast-forward"
    return "squash"


def format_merge(prs):
    styles = [s for s in map(merge_style, prs) if s]
    c = Counter(styles)
    return "merge: squash %d, fast-forward %d, merge commit %d (of %d)" % (
        c["squash"], c["fast-forward"], c["merge commit"], len(styles))


def recent_lines(prs):
    """Return one line per recent merged pull request, so a stage sees the naming conventions."""
    return ['recent: #%s %s "%s"' % (pr.get("number"), printable(pr.get("headRefName") or ""),
                                     printable(pr.get("title") or ""))
            for pr in prs[:RECENT_COUNT]] or ["recent: none"]


def key_forms(text):
    """Return the item key forms in a text, such as {"ABC-<n>"} for "ABC-12 fix the parser"."""
    return {m.group(1) + "-<n>" for m in ITEM_KEY.finditer(text)}


def common_key_form(texts):
    """Return the key form most texts carry, with the count of texts that carry it, or "none"."""
    counts = Counter(f for t in texts for f in key_forms(t))
    if not counts:
        return "none"
    form, n = counts.most_common(1)[0]
    return "%s %d/%d" % (form, n, len(texts))


def format_item_keys(prs):
    return "item keys: branches %s, titles %s" % (
        common_key_form([printable(p.get("headRefName") or "") for p in prs]),
        common_key_form([printable(p.get("title") or "") for p in prs]))


def format_ci(workflows, buildkite):
    parts = ["github-actions (%s)" % ", ".join(sorted(workflows))] if workflows else []
    parts += ["buildkite"] if buildkite else []
    return "ci: " + (", ".join(parts) or "none")


def issue_count(opened, closed, both):
    """Return the issues opened or closed in a window, from the three search counts."""
    return opened + closed - both


def release_candidates(logs, base_subjects):
    """Return (branch, picks, last date) for each branch with two or more picks from the base.

    logs maps a branch to the (date, subject) of each of its commits in the
    window that is not on the base. A pick is such a commit whose subject is
    the subject of a commit on the base, as a cherry-pick keeps it. The branch
    with the most picks comes first.
    """
    found = []
    for name, commits in logs.items():
        dates = [d for d, s in commits if s in base_subjects]
        if len(dates) >= 2:
            found.append((name, len(dates), max(dates)))
    return sorted(found, key=lambda c: (-c[1], c[0]))


def format_release_candidates(found):
    if not found:
        return "release candidates: none"
    return "release candidates: " + ", ".join(
        "%s (%d in %d days, last %s)" % (name, n, HISTORY_DAYS, last) for name, n, last in found)


def branch_state(name, prs):
    """Return (state, number) of a local branch from the pull requests whose head it is.

    An open pull request wins over older ones on the same branch, otherwise the
    newest one decides. The state is "no pull request" with no number when none
    has the branch as its head.
    """
    heads = [p for p in prs if p.get("headRefName") == name]
    pick = max([p for p in heads if p.get("state") == "OPEN"] or heads,
               key=lambda p: p.get("number") or 0, default=None)
    if pick is None:
        return "no pull request", None
    return (pick.get("state") or "").lower(), pick.get("number")


def branch_lines(branches, held, prs, reason):
    """Return one line per branch with an open pull request, and one per other state with names.

    held maps a branch to the worktree that has it checked out, so a stage sees
    which branches another checkout holds. prs is None when GitHub could not be
    read, and reason then says why.
    """
    def worktree(b):
        return " [worktree %s]" % held[b] if b in held else ""

    def named(b, n=None):
        return b + (" #%s" % n if n else "") + worktree(b)
    if not branches:
        return ["branch: none"]
    if prs is None:
        return ["%s %d (%s)" % (unknown("branch", reason), len(branches),
                                ", ".join(named(b) for b in branches))]
    states = [(b,) + branch_state(b, prs) for b in branches]
    lines = ["branch: %s open #%s%s" % (b, n, worktree(b)) for b, s, n in states if s == "open"]
    for kind in ("merged", "closed", "no pull request"):
        group = [named(b, n) for b, s, n in states if s == kind]
        if group:
            lines.append("branch: %s %d (%s)" % (kind, len(group), ", ".join(group)))
    return lines


def is_other_person(author, login):
    """Return True for an author who is a person other than the signed-in user, never a bot."""
    name = (dig(author, "login") or "")
    return bool(name) and dig(author, "__typename") != "Bot" \
        and not name.endswith("[bot]") and name.lower() != login.lower()


def comments_after(pr, pushed, login):
    """Return the comments other people wrote on a pull request after its last push.

    The count holds the comments on the conversation, the text of each review
    and the line comments of each review.
    """
    def counts(item, time_key):
        return (item.get(time_key) or "") > pushed and is_other_person(item.get("author"), login)
    talk = [c for c in nodes(pr.get("comments")) if counts(c, "createdAt")]
    reviews = [r for r in nodes(pr.get("reviews")) if counts(r, "submittedAt")]
    return len(talk) + sum((1 if (r.get("body") or "").strip() else 0)
                           + (dig(r, "comments", "totalCount") or 0) for r in reviews)


def open_threads(pr, login):
    """Return the unresolved review threads that another person started on a pull request."""
    return sum(1 for t in nodes(pr.get("reviewThreads")) if not t.get("isResolved")
               and is_other_person(dig(t, "comments", "nodes", 0, "author"), login))


def last_push(pr):
    """Return the time of a pull request's last push, as GitHub's ISO text.

    GitHub reports no push time for a commit, so this is the later of the
    head commit's commit time and the pull request's last force push.
    """
    return max(dig(pr, "commits", "nodes", 0, "commit", "committedDate") or "",
               dig(pr, "timelineItems", "nodes", 0, "createdAt") or "")


def format_pull_request(pr, login):
    """Return the line of one open pull request."""
    head = dig(pr, "commits", "nodes", 0, "commit") or {}
    pushed = last_push(pr)
    return "pull request: #%s %s -> %s %s checks %s merge %s review %s threads %d comments %d" % (
        pr.get("number"), printable(pr.get("headRefName") or ""),
        printable(pr.get("baseRefName") or ""), (pr.get("headRefOid") or "")[:12],
        dig(head, "statusCheckRollup", "state") or "none", pr.get("mergeStateStatus") or "none",
        pr.get("reviewDecision") or "none", open_threads(pr, login),
        comments_after(pr, pushed, login))


def format_approvals(prs):
    """Return each approving login with its count, most first, then the pull requests with none."""
    approvers = [{dig(r, "author", "login") for r in nodes(pr.get("reviews"))} - {None}
                 for pr in prs]
    counts = Counter(login for a in approvers for login in a)
    parts = ["%s %d" % (printable(login), n)
             for login, n in sorted(counts.items(), key=lambda c: (-c[1], c[0]))]
    return "approvals: " + ", ".join(parts + ["none %d" % sum(1 for a in approvers if not a)])


def plan_header(text):
    """Return the header values of a plan by key, from the first line that names each key."""
    values = {}
    for line in text.splitlines()[:PLAN_HEADER_LINES]:
        key, sep, value = line.partition(":")
        if sep and key in PLAN_KEYS and key not in values:
            values[key] = value.strip()
    return values


def format_plan(name, text):
    header = plan_header(text)
    return " | ".join(["plan: " + name]
                      + ["%s: %s" % (k, header[k]) for k in PLAN_KEYS if k in header])


def plans_lines(files):
    """Return the plans folder's lines from a map of file name to text, which only plans need."""
    names = sorted(files)
    plans = [format_plan(n, files[n]) for n in names if n.endswith("-plan.md")]
    return (plans or ["plan: none"]) \
        + ["seed report: " + n for n in names if n.endswith("-seed.md")] \
        + ["check file: " + n for n in names if n.endswith(CHECK_FILE_SUFFIXES)]


def section_headings(text):
    """Return the second-level headings of a Markdown text outside its code fences."""
    headings, fenced = [], False
    for line in text.splitlines():
        if line.startswith(("```", "~~~")):
            fenced = not fenced
        elif not fenced and line.startswith("## "):
            headings.append(line[3:].strip())
    return headings


def format_root_agents(text):
    if text is None:
        return "root AGENTS.md: none"
    return "root AGENTS.md: " + (", ".join(section_headings(text)) or "no sections")


def record_folder(paths):
    """Return (folder, record paths) of the tracked decision records, or (None, []).

    A record folder has one of the usual names and holds files whose names
    start with their number. With several, the shallowest one wins.
    """
    folders = {}
    for p in paths:
        folder = p.rpartition("/")[0]
        if folder.rpartition("/")[2] in RECORD_FOLDER_NAMES and p.rpartition("/")[2][:1].isdigit():
            folders.setdefault(folder, []).append(p)
    if not folders:
        return None, []
    folder = min(folders, key=lambda f: (f.count("/"), -len(folders[f]), f))
    return folder, folders[folder]


def adders(log):
    """Return the email of whoever added each path, from `git log --format=%x00%ae --name-only`.

    git lists the newest commit first, so a path added twice keeps its last addition.
    """
    added, email = {}, None
    for line in log.splitlines():
        if line.startswith("\0"):
            email = line[1:].strip().lower()
        elif line.strip():
            added.setdefault(line.strip(), email)
    return added


def format_records(folder, records, added, email):
    if folder is None:
        return "records: none"
    if not email:
        return "records: %s/ %d (unknown by you: no user.email)" % (folder, len(records))
    mine = sum(1 for r in records if added.get(r) == email.lower())
    return "records: %s/ %d (%d by you)" % (folder, len(records), mine)


def submodule_count(text):
    return sum(1 for line in text.splitlines() if line.strip().startswith("[submodule "))


def is_excluded(exclude_text):
    """Return True when an exclude file lists the local note, so git status stays clean."""
    return any(line.strip() == NOTE_EXCLUDE_LINE for line in exclude_text.splitlines())


def note_lines(path, text, excluded):
    """Return the local note's lines, its text whole and last, so no value follows it."""
    if text is None:
        return ["local note: none"]
    return ["local note (%s, excluded %s):" % (path, "yes" if excluded else "no"), text]


def render(lines):
    """Return the output text, the last line closed by a newline."""
    text = "\n".join(lines)
    return text if text.endswith("\n") else text + "\n"


# ---------------------------------------------------------------------------
# Running git and gh
# ---------------------------------------------------------------------------

def decode(data):
    return data.decode("utf-8", "replace")


def kill_group(p):
    """Kill a command that runs in its own session, with every process it started."""
    try:
        os.killpg(p.pid, signal.SIGKILL)
    except (AttributeError, OSError):
        p.kill()
    try:
        p.communicate(timeout=1)
    except subprocess.TimeoutExpired:
        pass


def run(args, cwd, seconds):
    """Return (exit status, stdout, stderr) of a command, as text.

    The status is None when the command cannot start or runs out of time, and
    stderr then holds the reason. The command gets its own session, so that a
    timeout also kills a helper such as ssh, which would keep the pipes open.
    """
    try:
        p = subprocess.Popen(args, cwd=cwd, env=dict(os.environ, **QUIET_ENV),
                             stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, start_new_session=True)
    except FileNotFoundError:
        return None, "", "%s not found" % args[0]
    except OSError as e:
        return None, "", "%s: %s" % (args[0], e.strerror or e)
    try:
        out, err = p.communicate(timeout=seconds)
    except subprocess.TimeoutExpired:
        kill_group(p)
        return None, "", "%s timed out after %d s" % (args[0], round(seconds))
    return p.returncode, decode(out), decode(err)


def runner(cwd, deadline):
    """Return a function that runs one command in cwd, within CALL_SECONDS and the deadline."""
    def call(*args):
        return run(list(args), cwd, max(0.5, min(CALL_SECONDS, deadline - time.monotonic())))
    return call


def stdout_or_reason(result, program):
    """Return (stdout, None) for a command that exited 0, else (None, reason)."""
    status, out, err = result
    if status == 0:
        return out, None
    if status is None:
        return None, err
    lines = [line.strip() for line in err.splitlines() if line.strip()]
    first = lines[0] if lines else "exit status %d" % status
    return None, printable("%s: %s" % (program, first))[:REASON_CHARS]


def git_out(call, *args):
    return stdout_or_reason(call("git", *args), "git")


def gh_out(call, *args):
    return stdout_or_reason(call("gh", *args), "gh")


def gh_json(call, *args):
    """Return (parsed JSON, None) of a gh command, or (None, reason)."""
    out, reason = gh_out(call, *args)
    if out is None:
        return None, reason
    try:
        return json.loads(out), None
    except ValueError:
        return None, "gh returned no JSON"


def graphql(call, query, **variables):
    """Return (data, None) of a GraphQL query, or (None, reason).

    Each variable goes to gh as a raw string field, which gh never reads as a
    file name or a number.
    """
    args = ["api", "graphql", "-f", "query=" + query]
    for k, v in sorted(variables.items()):
        args += ["-f", "%s=%s" % (k, v)]
    data, reason = gh_json(call, *args)
    if reason:
        return None, reason
    if not isinstance(dig(data, "data"), dict):
        return None, "gh returned no data"
    return data["data"], None


def read_file(path):
    """Return the text of a file, or None when it does not exist or cannot be read."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return None


# ---------------------------------------------------------------------------
# Reading the repository
# ---------------------------------------------------------------------------

def read_checkout(call, home):
    """Return (Checkout, None), or (None, the line a stage stops on)."""
    top, reason = git_out(call, "rev-parse", "--show-toplevel")
    if top is None:
        bare, _ = git_out(call, "rev-parse", "--is-bare-repository")
        if bare is not None and bare.strip() == "true":
            return None, BARE_MAIN
        return None, NO_REPOSITORY if reason.startswith("git:") else unknown("checkout", reason)
    top = top.strip()
    if same_path(top, home):
        return None, NO_REPOSITORY
    listing, reason = git_out(call, "worktree", "list", "--porcelain")
    common, common_reason = git_out(call, "rev-parse", "--path-format=absolute",
                                    "--git-common-dir")
    if listing is None or common is None:
        return None, unknown("checkout", reason or common_reason)
    trees = parse_worktrees(listing)
    if not trees or trees[0].bare:
        return None, BARE_MAIN
    return Checkout(top, trees[0].path, common.strip(), trees), None


def read_origin(call):
    """Return the "owner/repo" of origin, or None when origin is missing or not on GitHub."""
    url, _ = git_out(call, "remote", "get-url", "origin")
    return github_repo(url) if url else None


def read_login(call):
    out, reason = gh_out(call, "api", "user", "-q", ".login")
    return (out.strip(), None) if out and out.strip() else (None, reason or "gh returned no login")


def read_base(call, repo):
    """Return (base, None) from origin's HEAD, else GitHub's default branch, or (None, reason)."""
    ref, _ = git_out(call, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD")
    if ref and ref.strip().startswith("refs/remotes/origin/"):
        return ref.strip()[len("refs/remotes/origin/"):], None
    out, reason = gh_out(call, "repo", "view", repo, "--json", "defaultBranchRef",
                         "-q", ".defaultBranchRef.name")
    if not (out and out.strip()):
        return None, reason or "no default branch"
    return printable(out.strip()), None


def read_sync(call, base, fetched):
    """Return the local base against origin's, marked with the reason when the fetch failed.

    After a failed fetch the counts are those of the last fetch that worked.
    """
    if base is None:
        return unknown("base vs origin", "base unknown")
    out, reason = git_out(call, "rev-list", "--left-right", "--count",
                          "refs/heads/%s...refs/remotes/origin/%s" % (base, base))
    if out is None:
        return unknown("base vs origin", reason)
    ahead, _, behind = out.strip().partition("\t")
    _, fetch_reason = stdout_or_reason(fetched, "git")
    stale = " (fetch failed: %s)" % fetch_reason if fetch_reason else ""
    return "base vs origin: %s %s%s" % (ahead, behind.strip(), stale)


def read_tree(call):
    out, reason = git_out(call, "status", "--porcelain")
    if out is None:
        return [unknown("tracked changes", reason), unknown("untracked", reason)]
    tracked, untracked = status_counts(out)
    return ["tracked changes: %d" % tracked, "untracked: %d" % untracked]


def since_date(today):
    return (today - datetime.timedelta(days=HISTORY_DAYS)).isoformat()


TRACKER_QUERY = """
query($owner: String!, $name: String!, $opened: String!, $closed: String!, $both: String!) {
  repository(owner: $owner, name: $name) { milestones(states: OPEN) { totalCount } }
  opened: search(query: $opened, type: ISSUE, first: 0) { issueCount }
  closed: search(query: $closed, type: ISSUE, first: 0) { issueCount }
  both: search(query: $both, type: ISSUE, first: 0) { issueCount }
}"""


def read_tracker(call, repo, since):
    """Return the milestones and issues lines, the evidence of whether GitHub issues are in use."""
    owner, name = repo.split("/")
    scope = "repo:%s is:issue " % repo
    data, reason = graphql(call, TRACKER_QUERY, owner=owner, name=name,
                           opened=scope + "created:>=" + since, closed=scope + "closed:>=" + since,
                           both=scope + "created:>=%s closed:>=%s" % (since, since))
    if data is None:
        return [unknown("milestones", reason), unknown("issues", reason)]
    counts = [dig(data, k, "issueCount") or 0 for k in ("opened", "closed", "both")]
    return ["milestones: %d open" % (dig(data, "repository", "milestones", "totalCount") or 0),
            "issues: %d in %d days" % (issue_count(*counts), HISTORY_DAYS)]


MERGED_QUERY = """
query($owner: String!, $name: String!, $base: String!) {
  repository(owner: $owner, name: $name) {
    pullRequests(states: MERGED, baseRefName: $base, first: %d,
                 orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes { number title headRefName headRefOid mergeCommit { oid parents { totalCount } } }
    }
  }
}""" % MERGED_SAMPLE


def read_merged(call, repo, base):
    """Return (the last pull requests merged into the base, newest first, None), or (None, why)."""
    if base is None:
        return None, "base unknown"
    owner, name = repo.split("/")
    data, reason = graphql(call, MERGED_QUERY, owner=owner, name=name, base=base)
    if data is None:
        return None, reason
    return nodes(dig(data, "repository", "pullRequests")), None


MINE_QUERY = """
query($open: String!, $merged: String!) {
  viewer { login }
  open: search(query: $open, type: ISSUE, first: %d) { nodes { ... on PullRequest {
    number headRefName baseRefName headRefOid mergeStateStatus reviewDecision
    commits(last: 1) { nodes { commit { committedDate statusCheckRollup { state } } } }
    timelineItems(last: 1, itemTypes: [HEAD_REF_FORCE_PUSHED_EVENT]) {
      nodes { ... on HeadRefForcePushedEvent { createdAt } } }
    reviewThreads(first: 100) { nodes { isResolved
      comments(first: 1) { nodes { author { __typename login } } } } }
    comments(last: 100) { nodes { createdAt author { __typename login } } }
    reviews(last: 100) { nodes { submittedAt body author { __typename login }
      comments { totalCount } } }
  } } }
  merged: search(query: $merged, type: ISSUE, first: %d) { nodes { ... on PullRequest {
    reviews(states: APPROVED, first: 20) { nodes { author { login } } }
  } } }
}""" % (OPEN_PR_LIMIT, APPROVAL_SAMPLE)


def read_open_and_merged(call, open_query, merged_query):
    """Return (data, None) of the open and merged pull requests, or (None, reason).

    GitHub computes a pull request's merge state when it is first asked for it
    and answers UNKNOWN until then, so a query that meets UNKNOWN runs once more.
    """
    data, reason = graphql(call, MINE_QUERY, open=open_query, merged=merged_query)
    if data and any(pr.get("mergeStateStatus") == "UNKNOWN" for pr in nodes(data.get("open"))):
        again, _ = graphql(call, MINE_QUERY, open=open_query, merged=merged_query)
        data = again or data
    return data, reason


def read_mine(call, repo):
    """Return (the pull request lines and the approvals line, None), or (None, reason)."""
    scope = "repo:%s is:pr author:@me " % repo
    data, reason = read_open_and_merged(call, scope + "is:open sort:created-asc",
                                        scope + "is:merged sort:created-desc")
    if data is None:
        return None, reason
    login = dig(data, "viewer", "login") or ""
    lines = [format_pull_request(pr, login) for pr in nodes(data.get("open"))]
    return (lines or ["pull request: none"]) + [format_approvals(nodes(data.get("merged")))], None


def read_my_pull_requests(call, repo):
    """Return (the signed-in user's last pull requests here, None), or (None, reason).

    Each pull request holds its number, its head branch and its state.
    """
    prs, reason = gh_json(call, "pr", "list", "-R", repo, "--state", "all", "--author", "@me",
                          "--limit", str(PR_LIST_LIMIT), "--json", "number,headRefName,state")
    return (prs, None) if isinstance(prs, list) else (None, reason or "gh returned no list")


def read_pr_heads(call, repo, since):
    """Return (the heads of anyone's pull requests updated in the window, None), or (None, reason).

    The window is the one the picks are counted in, because a branch with
    commits in it updated its pull request in it too. A fixed number of pull
    requests reaches back less than 90 days in a busy repository, and the
    branches of older rebase merges then carry the base's subjects.
    """
    prs, reason = gh_json(call, "pr", "list", "-R", repo, "--state", "all",
                          "--search", "updated:>=" + since, "--limit", str(SEARCH_LIMIT),
                          "--json", "headRefName")
    if not isinstance(prs, list):
        return None, reason or "gh returned no list"
    return {p.get("headRefName") for p in prs if isinstance(p, dict)}, None


def read_local_branches(call, base):
    out, reason = git_out(call, "for-each-ref", "--format=%(refname)", "refs/heads")
    if out is None:
        return None, reason
    prefix = "refs/heads/"
    names = [line[len(prefix):] for line in out.splitlines() if line.startswith(prefix)]
    return [n for n in names if n != base], None


def read_branch_log(call, base, name, since):
    """Return (date, subject) of each commit of origin's branch in the window, not on the base."""
    out, _ = git_out(call, "log", "--no-merges", "--since=" + since, "--format=%cs%x00%s",
                     "refs/remotes/origin/%s..refs/remotes/origin/%s" % (base, name))
    return [tuple(line.split("\0", 1)) for line in (out or "").splitlines() if "\0" in line]


def read_release_candidates(call, pool, base, heads, since):
    """Return the release candidates line, from the base and (pull request heads, reason).

    A candidate is a branch of origin other than the base that is the head of
    no pull request updated in the window and holds picks from the base in it.
    A branch whose tip is older than the window holds no commit in it, so its
    log is not read.
    """
    pr_heads, heads_reason = heads
    if base is None or pr_heads is None:
        return unknown("release candidates", heads_reason or "base unknown")
    refs, reason = git_out(call, "for-each-ref", "--format=%(refname)%00%(committerdate:short)",
                           "refs/remotes/origin")
    subjects, subjects_reason = git_out(call, "log", "--no-merges", "--format=%s",
                                        "refs/remotes/origin/" + base)
    if refs is None or subjects is None:
        return unknown("release candidates", reason or subjects_reason)
    prefix = "refs/remotes/origin/"
    tips = [line.split("\0") for line in refs.splitlines()
            if line.startswith(prefix) and "\0" in line]
    names = [ref[len(prefix):] for ref, date in tips
             if date >= since and ref[len(prefix):] not in pr_heads | {base, "HEAD"}]
    logs = dict(zip(names, pool.map(lambda n: read_branch_log(call, base, n, since), names)))
    return format_release_candidates(release_candidates(logs, set(subjects.splitlines())))


def read_ci(top):
    folder = os.path.join(top, ".github", "workflows")
    try:
        workflows = [n for n in os.listdir(folder) if n.endswith((".yml", ".yaml"))]
    except OSError:
        workflows = []
    return format_ci(workflows, os.path.isdir(os.path.join(top, ".buildkite")))


def read_record_folder(call):
    """Return ((folder, record paths), None) of the tracked records, or (None, reason)."""
    paths, reason = git_out(call, "ls-files", "-z")
    if paths is None:
        return None, reason
    return record_folder([p for p in paths.split("\0") if p]), None


def read_records(call):
    """Return the records line: the record folder, its records, and how many of them you added."""
    found, reason = read_record_folder(call)
    if found is None:
        return unknown("records", reason)
    folder, records = found
    if folder is None:
        return format_records(None, [], {}, None)
    # Without --no-renames, a record that was renamed shows as a rename and not as an addition.
    log, _ = git_out(call, "log", "--no-renames", "--diff-filter=A", "--format=%x00%ae",
                     "--name-only", "--", folder)
    email, _ = git_out(call, "config", "user.email")
    return format_records(folder, records, adders(log or ""), (email or "").strip())


def read_docs(call, top):
    """Return the records, root AGENTS.md and submodules lines of the checkout."""
    return [read_records(call),
            format_root_agents(read_file(os.path.join(top, "AGENTS.md"))),
            "submodules: %d" % submodule_count(read_file(os.path.join(top, ".gitmodules")) or "")]


def read_plans(folder):
    """Return the plans folder's lines. A folder that does not exist yet holds no plan."""
    try:
        names = [n for n in os.listdir(folder) if os.path.isfile(os.path.join(folder, n))]
    except FileNotFoundError:
        names = []
    except OSError as e:
        return [unknown("plan", "%s: %s" % (folder, e.strerror or e))]
    return plans_lines({n: (read_file(os.path.join(folder, n)) or "") if n.endswith("-plan.md")
                        else "" for n in names})


def read_note(checkout):
    """Return the local note's lines, from the main checkout, which every worktree shares."""
    path = os.path.join(checkout.main, NOTE_PATH)
    exclude = read_file(os.path.join(checkout.common, "info", "exclude")) or ""
    return note_lines(path, read_file(path), is_excluded(exclude))


# ---------------------------------------------------------------------------
# The report
# ---------------------------------------------------------------------------

def owner_line(login, repo):
    """Return the ownership line from (login, reason)."""
    who, reason = login
    if who is None:
        return unknown("owner", reason)
    return "owner: " + ("own" if is_own(who, repo) else "shared")


def history_lines(merged):
    """Return the merge style line and the recent lines from (merged pull requests, reason)."""
    prs, reason = merged
    if prs is None:
        return [unknown("merge", reason), unknown("recent", reason)]
    return [format_merge(prs)] + recent_lines(prs)


def item_keys_line(merged):
    prs, reason = merged
    return unknown("item keys", reason) if prs is None else format_item_keys(prs)


def branch_section(local_branches, worktrees, my_prs):
    """Return the branch lines from (local branches, reason) and (pull requests, reason)."""
    names, reason = local_branches
    if names is None:
        return [unknown("branch", reason)]
    held = {t.branch: t.path for t in worktrees if t.branch}
    return branch_lines(names, held, *my_prs)


def mine_lines(mine):
    """Return the open pull request lines and the approvals line from (lines, reason)."""
    lines, reason = mine
    if lines is None:
        return [unknown("pull request", reason), unknown("approvals", reason)]
    return lines


def report_lines(call, pool, checkout, repo, home, since):
    """Return every line after the stopping cases, in the order a stage reads them.

    The network calls start first and run side by side, and the local reads run
    while they wait. The base is read before the call that needs it: from
    origin's HEAD at once, or from GitHub, which costs one call in turn.
    """
    fetch = pool.submit(call, "git", "fetch", "--quiet", "origin")
    login = pool.submit(read_login, call)
    tracker = pool.submit(read_tracker, call, repo, since)
    mine = pool.submit(read_mine, call, repo)
    my_prs = pool.submit(read_my_pull_requests, call, repo)
    heads = pool.submit(read_pr_heads, call, repo, since)
    base, base_reason = read_base(call, repo)
    merged = pool.submit(read_merged, call, repo, base)
    tree = read_tree(call)
    ci = read_ci(checkout.top)
    local_branches = read_local_branches(call, base)
    plans = read_plans(plans_dir(home, repo))
    docs = read_docs(call, checkout.top)
    note = read_note(checkout)
    fetched = fetch.result()
    return ([format_checkout(checkout.top, checkout.main), "github: " + repo,
             "plans: " + plans_dir(home, repo), owner_line(login.result(), repo),
             "base: " + base if base else unknown("base", base_reason),
             read_sync(call, base, fetched)]
            + tree + history_lines(merged.result()) + [ci] + tracker.result()
            + [item_keys_line(merged.result()),
               read_release_candidates(call, pool, base, heads.result(), since)]
            + branch_section(local_branches, checkout.worktrees, my_prs.result())
            + mine_lines(mine.result()) + plans + docs + note)


def report(cwd, home, today, deadline):
    """Return the output lines for a stage started in cwd, or the one line it stops on."""
    call = runner(cwd, deadline)
    checkout, stop = read_checkout(call, home)
    if stop:
        return [stop]
    repo = read_origin(call)
    if repo is None:
        return [NO_GITHUB]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        return report_lines(call, pool, checkout, repo, home, since_date(today))


def main():
    """Print the report and exit 0, whatever went wrong on the way."""
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    deadline = time.monotonic() + SCRIPT_SECONDS
    try:
        lines = report(os.getcwd(), os.path.expanduser("~"), datetime.date.today(), deadline)
    except Exception as e:  # the stage reads this line instead of a traceback
        lines = [unknown("repo_state", "%s: %s" % (type(e).__name__, e))]
    sys.stdout.write(render(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
