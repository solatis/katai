---
name: standards
description: The standards of the katai stages -- one rule file per subject, how a repository departs from a rule, the checks after a change, and the repair of existing code and documents. Loaded before code, a plan or a document is written.
user-invocable: false
---

# Standards

This skill is a guide. A standard is a rule file in this skill's directory
for one subject, one set for every repository. The guide says how the
standards are applied, checked and departed from, and its references show
examples. Read the rule file of a subject before you write anything of that
subject.

Where documents live and what they hold is the repository's own policy. It is
the "Documentation strategy" section of the root `AGENTS.md`, which the
stage's `root AGENTS.md:` line shows, and the `AGENTS.md` of the
documentation folder that the section names (`doc/` or `docs/`). Read them
where they exist.

## Where a repository departs from a rule

A rule file here is the default. A sentence in the repository's instruction
files outranks a sentence in the owner's own configuration, and both outrank
a rule file here. A departure is one sentence that names the rule it departs
from, says what holds instead and why, and carries its date.

What the code or the tests of a repository already do is never a rule,
however often they do it. Where they do what a rule here forbids and no
sentence says so, the change follows the rule in what it adds, and a design
that follows the existing code instead is a Rationale row of the plan marked
`proposal`.

A sentence that conflicts with a rule here and does not name it may be a
departure or may be older than the rule. It is a question for the owner,
asked once, when a commit of the unit would meet the conflict. The answer is
kept as one sentence, so that it is not asked again. The seed's report says
where this repository keeps its rules for the subject, and the sentence goes
there.

## What a change is held to

- Comments and documents: whole files where `owner: own`, and the lines the
  change adds or rewrites where `owner: shared`, as "Held to the owner's
  lines" says below.
- Code and tests: what the change adds or rewrites, in every repository.
  Rule 18 of `code.md` and rule 17 of `tests.md` say so. Bringing existing
  code or tests under the rules changes what the code does or what is
  verified, so it is work of its own and never part of another change.
- Names: the names the change introduces.

How the language spells a rule, such as the library that draws test inputs
or the lint that carries a rule for code, is read from the tree. A fact of
one repository, such as a port, a fixture or a command, lives in its
instruction files. Neither is written into a rule file here.

The guide works from what the stage printed. Where no stage printed an
`owner:` line, the repository counts as shared.

## Where a reason lands

A reason lands on the rung of the ladder in `placement.md` that covers its
subject. The stage's `owner:` line decides where a change may write.

- `owner: own`: every rung that the "Documentation strategy" lays out, such
  as the code comments, the Why entries of a component `AGENTS.md` and the
  decision records.
- `owner: shared`: a comment on the lines the change adds or rewrites, a file
  in the repository that the owner already keeps there, such as a decision
  record the owner wrote, changed in the change's pull request, or the local
  note. `git log --diff-filter=A -- <file>` shows who added a file. Nothing is
  written into a document or an instruction file that another person keeps,
  such as a root `AGENTS.md` that others maintain, and in code the change
  comments only its own lines.

Where the repository has no "Documentation strategy":

- In the owner's own repository, the first unit's plan proposes the base
  structure as a `docs` commit, and the owner approves it with the plan. The
  structure is a root `AGENTS.md` with a "Documentation strategy" section,
  and the `AGENTS.md` files with their Map tables that the ladder of
  `placement.md` assumes.
- In a shared repository, a documentation structure is work of its own. The
  owner starts it as a unit, and it reaches the repository through a pull
  request that the others see. Until then a reason lands as `owner: shared`
  says above.
- The repair of existing code and documents below does not run.

## Files

| File                      | Read it                                                                                     |
| ------------------------- | ------------------------------------------------------------------------------------------- |
| `comments.md`             | before you write or change code or a sketch: the rules for comments                         |
| `prose.md`                | before you write a sentence of a comment or a document                                      |
| `narrative.md`            | before you write or change code, or the sketches of a plan                                  |
| `placement.md`            | before you write or move a document, or a comment that holds knowledge                      |
| `names.md`                | before you name a type, a trait, a function, a field, a module or a file                    |
| `code.md`                 | before you sketch or write a function, a type or a module                                   |
| `tests.md`                | before you sketch or write a test                                                           |
| `checks.md`               | after a change is complete, before it leaves the session                                    |
| `scripts/check_steps.py`  | the step check: it checks walkthrough numbers, back-references and denied marks             |
| `scripts/change_parts.py` | the part list: it splits a change, or the files under given paths, into parts for `kt:read` |

## The scripts

The scripts are in `scripts/` under this skill's base directory, which the
first line of this guide names when it loads ("Base directory for this
skill"). Run them by that absolute path, so that they work in any checkout and
any directory. The step check runs in one of five forms:

```
python3 <base directory>/scripts/check_steps.py --plan <plan.md>
python3 <base directory>/scripts/check_steps.py [--deny REGEX]... [--warn] <path>...
python3 <base directory>/scripts/check_steps.py [--deny REGEX]... --git-range <base>...<rev> [--markdown-too] [--lines <base>...<rev>]
python3 <base directory>/scripts/check_steps.py --markdown <file.md>
python3 <base directory>/scripts/check_steps.py --words <any words>
```

`--plan` checks the sketches of a plan as `--markdown` does, and also its
Tests part: each test sketch names its kind, what it pins, why it has its
level and its fakes. Step 1 of `checks.md` names the deny patterns. `--lines <range>` keeps only
the findings on the lines that `git diff -U0 <range>` adds or changes. For a
git range, the check prints one line `skipped <path>: <reason>` on stderr,
before the findings, for each changed file whose comment syntax it does not
know, such as a build file or a test script, and for each directory it
leaves out, such as `vendor/`, with the count of its changed files. The last
line on stdout is
`check_steps: <n> findings in <m> files`. Exit status 0 means no finding, 1
means findings, and 2 means a usage or git error. A skipped file is no
finding.

## The checks that run in a subagent

Four companion skills run in a subagent of their own: `kt:read` on the
agent `kt:cold-reader`, `kt:audit` on the agent `kt:auditor`, and
`kt:attack-plan` and `kt:attack-build` on the agent `kt:attacker`. The
cold reader knows no rule and no plan and reports where it stops. The
auditor knows the rules and reports each line that breaks one. The
attacker knows the claims and no rule, and reports each claim it broke
with the case that breaks it. An agent
file says how its reader thinks, and the skill says what it reads and how
it answers. Call each through the
Skill tool, with the words after its name as its arguments. The subagent sees
none of the conversation, and its last message comes back to the caller. The
skill passes its first words to a script, so each of them is one plain word
without quotes or spaces.

- `kt:read` takes the range of a change, or one or more paths joined
  by commas, and the number of one part, and nothing else. For paths, the
  parts hold the tracked files under them whole. The script leaves out the
  files it also leaves out of a range, such as lock files and binary files.
  The script splits a range into parts of about 300 changed lines, and paths
  into parts of about 300 lines. One reader reads each part. A reader who has
  not seen the change reads the files as they are on disk, every changed text
  file included. It returns one row for each line where it stopped, each
  function whose plan it had to rebuild, each comment that told it nothing,
  each walkthrough item that repeats its code, each statement it believes
  false, each doc comment that does not say with a verb what its function
  does, each sentence it had to untangle, each term the code defines that a
  comment uses before any comment explains it, and each term or statement in
  a document it could not place.
- `kt:audit <scope> [lines] [plan: <plan>] [focus: ...] [also: ...]`
  takes a range or one path. `lines` holds it to the lines the change adds or
  rewrites. It may also take a plan to reconcile against, a focus that limits
  the checks, and the paths of documents that belong to the task, which the
  subagent reads itself. It returns the report of the "Report" section below,
  with each change it proposes as a row. Without a focus it audits comments
  and documents. With `focus: code` it holds the scope against `code.md` and
  `names.md`, and with `focus: tests` against `tests.md`, each in a run of
  its own, so that no run reads every rule file. The scope of those two is a
  range held to `lines`, or the path of a plan, whose Design and Tests part
  are then audited before any code exists.

- `kt:attack-plan <plan>` takes the path of one plan, and
  `kt:attack-build <base>...HEAD` the range of a built change, and nothing
  else. Each returns one row per finding, then what held and what it could
  not read.

The caller of an attack passes the plan or the range alone, for the same
reason as the caller of `kt:read`. The caller of `kt:read` passes the range or the paths and the part
number alone, because the reader is useful only while it does not know what
the author knows. The caller of `kt:audit` adds facts about the task,
and never its view of the result.

## Held to the owner's lines

Where the stage printed `owner: shared`, the checks judge only the lines that
the change adds or rewrites. Where it printed `owner: own`, every check covers
whole files. "Held to the owner's lines" in `checks.md` says how each check
is held to those lines: the step check takes `--lines <base>...HEAD`, a
reader's stop on a line the change does not touch is declined with that
reason, and `kt:audit` gets the token `lines`. A comment block that
another author wrote is not rewritten whole. A finding in it is listed in the
review's "Checks" and left. Rule 13 of `comments.md`, which
rewrites a touched block whole, holds for the owner's own blocks.

## Who writes

The session that owns a change writes its comments and documents. It writes
each reason from evidence it can name: a line of code, a test, a document it
moves or a commit. It asks the owner for a reason it has no evidence for. Ask
the owner the way the owner's instructions say, and end your turn until the
answer comes; where they say nothing, ask in this conversation. An agent that
the session starts reports and writes nothing. The companion skills run on
agents that have no tool that writes, so they cannot change a file.

## Hard limits

These limits hold for the comments and documents of a change and for their
repair.

1. Comments and documentation files only. When existing code is repaired,
   never change what code does: no renames, no reordering, no refactors, no
   formatting sweeps. If code should change (a function that needs
   splitting, a misleading name, dead code), put it in the report.
2. Never invent rationale. A comment may only state what you verified from the
   code, the tests, the docs you are moving, or git history. If the "why" is
   unknown, write the "what" and ask the owner for the reason.
   `kt:audit` lists the gap under "Rationale unknown" as a question.
   Every "why" you intend to write names its evidence in the plan table of
   `narrative.md` or `placement.md`: a `file:line`, a test, the passage being
   moved, or a commit. The evidence stays in the plan; it does not go into
   the comment.
3. A wrong comment is worse than none. Verify every existing comment you touch
   against the code. Fix or delete stale ones, and never leave one you know
   is wrong. A comment that reads as a patch on an earlier version, or that
   mentions a plan, a review, an issue or the conversation, counts as wrong
   even when each clause is true. It is rewritten whole from the code. Held
   to the owner's lines, this holds for the owner's own blocks, and a block
   of another author is reported as the section above says.
4. Code that needs a comment gets it. A missing note at a line where the
   reader stops is as much a defect as a note that repeats its line. A
   function that qualifies for a walkthrough under `comments.md` gets one,
   whether or not any reader stopped in it. Deleting a comment that fails the
   cut pass in `narrative.md` is as much the job as writing a missing one.
5. ASCII only. Match the comment syntax, doc-comment convention and line width
   of the surrounding file.
6. Moving is cut-and-paste, not copy. After a move the knowledge exists once,
   at the most local place, and every other mention is a pointer or is gone.

## Repairing existing code and documents

A session that is asked to bring existing code and documents under the rules
works as follows:

1. Read `comments.md`, `prose.md` and the repository's policy files. If the root `AGENTS.md`
   has no "Documentation strategy" section, stop and say so; the repair runs
   only where the repository has one.
2. Run `kt:audit <path>` for one component directory at a time, leaf
   directories first. Several `kt:audit` calls for independent
   components may run side by side. Keep each report as it came back.
3. Apply each report row by row. Write a reason only from the evidence its
   row names, or from evidence you find yourself. Ask the owner for each
   reason that has no evidence, and write that comment after the answer
   arrives. A row you do not apply is declined with its reason.
4. Verify. After editing Markdown, run `npx prettier --write` on the touched
   files. Do not run a code formatter. Review `git diff` hunk by hunk: every
   changed line in a source file must be a comment line. Revert any hunk that
   changes a non-comment token and redo it by hand. Run the step check over
   the changed files and fix each finding until it reports none. Run the
   build or tests when that is cheap.
5. Follow `checks.md` over the commits of the repair, with one difference in
   the first reader round, which is step 2 of `checks.md`. Where that step
   lists the parts of the range of the change, a repair lists the parts of the
   paths that it gave to `kt:audit`, so that a reader also reads the
   functions that the repair left as they were. The second reader round, step
   4 of `checks.md`, reads its range as `checks.md` says.
6. Report, in the form of the "Report" section, with the rows applied and
   declined.

## Reconciling against a plan document

A plan document says what the comments and documents were going to be,
written while the reasons were still in context; the code says what they
became. The gap between the two is where reasons get lost, because the plan
is deleted once its work lands. `kt:audit` follows these steps when
its caller names a plan:

1. Collect every promise the plan makes about prose: each claim in the
   sketches of its design section, and each row of its rationale table with
   the landing place its knowledge section gives it (a decision record, an
   `AGENTS.md` row, a code comment, the local note, or `plan only`).
2. Skip the `plan only` rows. The plan drops them on purpose.
3. Hold every other promise to the cut pass in `narrative.md` before
   looking for it. A promise that fails the cut pass is not written, even
   when the plan asks for it: it repeats the code, it names a rejected
   alternative no reader of that line would propose, or it records the
   conversation. List it under "Dropped on purpose".
4. For each remaining promise, find where it landed. A changed wording is
   fine when the claim survives. A claim that is gone is a finding.
5. Each finding becomes one row of the narrative or placement plan table,
   with the plan as its evidence for each reason, so the session that applies
   the report writes the missing reason where the plan said it would go. A
   promise the code contradicts (the design changed while building) is not
   written. It goes under "Needs a human" with both versions quoted.
6. Report the findings under "Unlanded from the plan", one line each: the
   promise, where the plan said it would land, what is there instead.

## Report

Keep the report short, and list its rows. `kt:audit` writes the Run
line first, then its plan tables, then each other section as proposed
changes. A session that repairs code writes each section as changes made.

- Run: one line that repeats the caller's words verbatim, then the scope, the
  last line of the step check, and the number of functions at each level
  (bare, notes, walkthrough).
- Moved: from -> to, one line each.
- Commented: functions whose comments were written or rewritten.
- Removed: stale, duplicate, historical or noise comments and doc passages.
- Discoverability: `AGENTS.md` Map rows added or changed.
- Wording: sentences in comments or documents that break the rules of
  `prose.md`, each with the rule it breaks.
- Rationale unknown: places where the why could not be verified, each as a
  question for the owner.
- Unlanded from the plan: reasons the plan document promised that no comment
  or document states; "none" when a plan was given and all landed.
- Dropped on purpose: plan promises that failed the cut pass, one line each
  with the defect.
- Code, Tests: with `focus: code` or `focus: tests`, one row per line that
  breaks a rule, as `<path>:<line> | <rule file> rule <n> | <what is
there> | <the change, or the question>`. A line that breaks no rule the
  reader can cite gets no row.
- Needs a human: code-level findings outside this skill's limits (split
  candidates, misleading names, dead or commented-out code, doc budget
  overruns that cannot be fixed by moving).
