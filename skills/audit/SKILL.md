---
name: audit
description: Audits code, tests, documents or a plan against one subject of the katai standards and the policy of the repository, and returns the changes they call for as rows of a report. The checks of `kt:standards` run it, and it changes no file.
context: fork
agent: kt:auditor
background: false
user-invocable: false
argument-hint: "<base>...HEAD | <path> [lines] [plan: <plan>] [focus: ...] [also: ...]"
allowed-tools: Bash(git diff:*), Bash(grep:*), Bash(true), Bash(python3 "${CLAUDE_SKILL_DIR}/../standards/scripts/check_steps.py" *)
---

# Audit against the standards

The caller's words: $ARGUMENTS

You audit the scope against the rule files of one subject. Without a
`focus:` of `code` or `tests`, the subject is comments and documents.

## The changed lines

!`git diff -U0 --no-color $0 2>/dev/null | grep -E '^(\+\+\+ |@@ )' || true`

When the scope is a range, each `+++ b/<path>` line names a changed file, and
each `@@ ... +<start>,<count> @@` line below it names changed lines in that
file as it is on disk now. When the scope is a path, you read every file in
scope whole and set this block aside.

## The step check

!`python3 "${CLAUDE_SKILL_DIR}/../standards/scripts/check_steps.py" --warn --words $0 2>&1 || true`

A line whose rule is `W1`, `W2` or `W3` is a warning, and you judge whether
it calls for a row. A line `skipped <path>: <reason>` names a changed file
that the step check cannot read, or a directory of changed files that it
leaves out. You read each such file that the scope holds like every other
file in scope.

## The caller's words

- The first word is the scope: a range `<base>...HEAD`, or one path of a file
  or a directory.
- `lines`, after the scope, holds the audit to the lines that the change adds
  or rewrites, because the repository belongs to other people as well. A row
  names only a line that the block of changed lines covers, and a finding of
  the step check on another line is no row. A row whose change reaches lines
  outside the change, as rule 13 of `comments.md` asks for a touched
  comment block, names those lines, and the caller decides on it. You propose
  no move into a document that the change does not touch.
- `plan:` is followed by the path of the plan to reconcile against. You read
  the plan from that path.
- `focus:` is followed by one or more of `placement`, `comments`, `wording`
  and `numbering`, or by `code` or `tests` alone. You run only those checks.
  Without a focus you run the four checks of comments and documents. `code`
  and `tests` run only when named, each in a run of its own, and "Code and
  tests" below says what such a run reads and reports.
- `also:` is followed by the paths of documents that belong to the task. You
  read each of them.
- The scope leaves out generated code, vendored code, lock files and every
  file that git ignores. For a path in scope, you still read the `AGENTS.md`
  chain from the root down to it, but you report only knowledge that
  concerns that path.

## What you read

1. The rules: `${CLAUDE_SKILL_DIR}/../standards/comments.md` and
   `${CLAUDE_SKILL_DIR}/../standards/prose.md`, whole. The
   policy of the repository: the "Documentation strategy" section of the root
   `AGENTS.md`, and the `AGENTS.md` of the documentation folder that the
   section names, where they exist.
2. `${CLAUDE_SKILL_DIR}/../standards/SKILL.md`, whole.
3. `${CLAUDE_SKILL_DIR}/../standards/narrative.md` when the scope holds
   code or tests. You apply it to each function in scope.
4. `${CLAUDE_SKILL_DIR}/../standards/placement.md` when the scope holds
   Markdown. You apply it, and the rules of the documentation folder's
   `AGENTS.md`, to each document in scope.
5. The documents of the change: each `AGENTS.md` from the root down to each
   path in scope, each decision record that the code in scope cites, and the
   paths after `also:`.
6. Each changed function and each changed section of a document, whole, in
   every changed text file.

## Code and tests

With `focus: code` or `focus: tests` you set aside "What you read" above
and the checks below, and you read:

1. `${CLAUDE_SKILL_DIR}/../standards/SKILL.md`, the sections "Where a
   repository departs from a rule" and "What a change is held to".
2. For `code`: `${CLAUDE_SKILL_DIR}/../standards/code.md` and
   `${CLAUDE_SKILL_DIR}/../standards/names.md`. For `tests`:
   `${CLAUDE_SKILL_DIR}/../standards/tests.md`.
3. Each `AGENTS.md` from the root down to each path in scope, and the paths
   after `also:`. A sentence there that departs from a rule decides, and a
   line it covers gets no row.
4. The plan after `plan:`, where one is named: its Rationale, and for
   `tests` its Tests part.
5. The scope. For a range, each changed function or test, whole, and you
   report only on the lines the change adds or rewrites. For the path of a
   plan, its Design and its Tests part, and each row then names a line of
   the plan.

For `code`, hold each added or rewritten function, type and module against
each rule of `code.md`, and each new name against `names.md`.

For `tests`, hold each added or rewritten test against each rule of
`tests.md`. Say for each test what it touches, and from that which kind it
is: a test that starts a process of the program under test is end-to-end,
whatever its plan or its file calls it. Report a test whose kind by what it
touches differs from the kind its plan entry names, a test at a kind higher
than the lowest that reaches its behavior, a fake of a subsystem that no
Rationale row names, and a case enumerated at two levels. With a plan, also
report each entry of the Tests part that no test carries, under "Unlanded
from the plan".

Your answer is the Run line and then the section `Code` or `Tests` of the
guide's "Report", one row per finding, and "Unlanded from the plan" where a
plan was named. A scope with no finding gets the one line `no rows`.

## The checks

- `placement`: where each piece of knowledge lives, by `placement.md`.
- `comments`: the level of each function and its comments, by
  `narrative.md`, with the cut pass and the gaps.
- `wording`: each sentence of a comment or document in scope against the
  rules of `prose.md`.
- `numbering`: the step check above. Each of its findings is a row. The step
  check above runs without deny patterns, so you search the comments in scope
  with Grep for the two forms that rule 16 of `comments.md` forbids: the
  path of the repository's folder of decision records, and `(owner,`.

When a plan is named, follow "Reconciling against a plan document" in the
guide. A reason that nothing supports is a question under "Rationale
unknown".

## Your answer

Your answer starts with the Run line of the guide's "Report" section, which
repeats the caller's words verbatim. The plan tables of `narrative.md` and
`placement.md` follow, and then the other sections of the report. Add nothing
before the Run line or after the report.

You are done when you have run each check of the focus over every file in
scope and written one row for each finding.
