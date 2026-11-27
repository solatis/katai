#!/usr/bin/env python3
"""Run the step check over each open pull request of the signed-in user, for the merge stage.

The merge stage runs this script when it loads, with no argument. For each
open pull request of the signed-in user in this repository, oldest first, it
runs `check_steps.py` of the doc-discipline skill over the range
`origin/<base>...origin/<head>` and prints one line, `#<n> <head>: ` and the
last line the check printed. That line counts the findings when the check ran,
and says why when it did not. The merge reads it here, because CI does not run
the check and a message that says the check passed is a claim.

Where the repository is shared, the check judges only the lines that the range
adds or changes. It denies comments that cite the record folder by its path,
because a comment cites a record by its number, and the `(owner, <date>)`
mark, because a comment does not say who decided something.

The script reads the repository as `repo_state.py` does, prints that script's
line when a stage stops, always exits 0 and ends within 60 seconds.
"""

import concurrent.futures
import os
import re
import sys
import time

# Importing repo_state would otherwise write its compiled form into the plugin's folder.
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import repo_state as rs  # noqa: E402

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK_STEPS = os.path.join(PLUGIN_ROOT, "skills", "doc-discipline", "scripts", "check_steps.py")
OWNER_MARK = r"\(owner,"


def check_arguments(base, head, folder, shared):
    """Return the options of check_steps.py for one pull request."""
    span = "origin/%s...origin/%s" % (base, head)
    deny = ([re.escape(folder) + "/"] if folder else []) + [OWNER_MARK]
    return ([a for d in deny for a in ("--deny", d)] + ["--git-range", span, "--markdown-too"]
            + (["--lines", span] if shared else []))


def last_line(result):
    """Return the last line of a check: its count of findings, or the reason it did not run.

    check_steps.py exits 0 or 1 after it ran and 2 when it could not run, and
    then the reason is on stderr.
    """
    status, out, err = result
    if status is None:
        return err
    lines = [line for line in (out if status in (0, 1) else err).splitlines() if line.strip()]
    return lines[-1] if lines else "check_steps: no output, exit status %d" % status


def check_pull_request(call, pr, folder, shared):
    head = pr.get("headRefName") or ""
    result = call(sys.executable, "-B", CHECK_STEPS,
                  *check_arguments(pr.get("baseRefName") or "", head, folder, shared))
    return "#%s %s: %s" % (pr.get("number"), rs.printable(head), rs.printable(last_line(result)))


def read_open_pull_requests(call, repo):
    """Return (the signed-in user's open pull requests here, None), or (None, reason).

    The oldest comes first, which puts the bottom of a stack before the pull
    requests on it.
    """
    prs, reason = rs.gh_json(call, "pr", "list", "-R", repo, "--state", "open", "--author", "@me",
                             "--limit", str(rs.PR_LIST_LIMIT),
                             "--json", "number,headRefName,baseRefName")
    if not isinstance(prs, list):
        return None, reason or "gh returned no list"
    return sorted((p for p in prs if isinstance(p, dict)),
                  key=lambda p: p.get("number") or 0), None


def report(cwd, home, deadline):
    """Return one line per open pull request, or the one line the stage stops on."""
    call = rs.runner(cwd, deadline)
    checkout, stop = rs.read_checkout(call, home)
    if stop:
        return [stop]
    repo = rs.read_origin(call)
    if repo is None:
        return [rs.NO_GITHUB]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        login = pool.submit(rs.read_login, call)
        prs, reason = read_open_pull_requests(call, repo)
        if prs is None:
            return [rs.unknown("step check", reason)]
        if not prs:
            return ["step check: no open pull request of yours"]
        found, _ = rs.read_record_folder(call)
        folder = found[0] if found else None
        who, _ = login.result()
        # An unknown owner reads as shared, so the check never judges other people's lines.
        shared = who is None or not rs.is_own(who, repo)
        at_top = rs.runner(checkout.top, deadline)
        return list(pool.map(lambda pr: check_pull_request(at_top, pr, folder, shared), prs))


def main():
    """Print the lines and exit 0, whatever went wrong on the way."""
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    deadline = time.monotonic() + rs.SCRIPT_SECONDS
    try:
        lines = report(os.getcwd(), os.path.expanduser("~"), deadline)
    except Exception as e:  # the stage reads this line instead of a traceback
        lines = [rs.unknown("step check", "%s: %s" % (type(e).__name__, e))]
    sys.stdout.write(rs.render(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
