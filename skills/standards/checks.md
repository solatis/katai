# The checks after a change

The session that owns a change runs these checks after its last code commit
and before the change leaves the session. The checks run in the order of how
much their fixes change. The attack comes first, because a finding of it changes
what the code does. The audits of code and tests follow, because a row of
theirs changes code. The checks of comments follow, because they
read the code as it then is. Each check is a script's output or
another agent's answer, and the session saves each answer where the stage
says. `<base>` is the revision the change started from. `<base directory>` is
the absolute path of this skill's directory, which the first line of the
loaded guide names.

## Held to the owner's lines

Where the stage printed `owner: shared`, the checks judge only the lines that
the change adds or rewrites, because the rest of the code belongs to other
people. An `owner:` line that reads `unknown`, or none, counts as shared.
Where the stage printed `owner: own`, every check covers whole files.

- The step check runs with `--lines <base>...HEAD`, in steps 1 and 6.
- A reader's stop on a line that the change does not touch is declined with
  the reason "outside the change", in step 3.
- `kt:audit` gets the token `lines` after the range, in step 5.
- A comment block that another author wrote, as `git blame` shows, is not
  rewritten whole. A finding in it is listed under "Checks" in the
  review and left as it is. Rule 13 of `comments.md`, which
  rewrites a touched block whole, holds for the owner's own blocks.

## The attack

Before every other check, run `kt:attack-build <base>...HEAD`, with the
range and no other word. The attacker reads the changed code and tests and
what they say about themselves, and no plan. Save its answer verbatim. Close
each finding in one of three ways: a fix with the test that pins it, a
question to the owner, or a decline with the line of code or the test that
refutes the case. The attack runs once.

## Code and tests

Before the steps below, when the change adds or rewrites code, run
`kt:audit <base>...HEAD lines focus: code`, and when it adds or rewrites
tests, run `kt:audit <base>...HEAD lines focus: tests`. A change with a
plan adds `plan: <plan>`, and the tests audit then also holds each test
against its entry in the plan's Tests part. Both carry `lines` in every
repository, because code and tests are held only to what a change adds or
rewrites. Save each report verbatim. Close each row in one of three ways: a
commit that changes the code or the test, a question to the owner, or a
decline with its reason. A row about a line the change did not add or
rewrite is declined as outside the change.

## The steps

1. Run the step check over what the change touched, and fix and commit each
   finding:

   ```
   python3 <base directory>/scripts/check_steps.py \
     --deny '<record folder>' --deny '\(owner,' \
     --git-range <base>...HEAD --markdown-too [--lines <base>...HEAD] 2>&1
   ```

   `<record folder>` is the folder that the stage's `records:` line names,
   such as `doc/adr/`. Where that line names no folder, leave its `--deny`
   out. `--lines` is there where the checks are held to the owner's lines.
   Keep each line `skipped <path>: <reason>` for the review. The step check
   cannot read the file such a line names, and the readers of step 2 read
   it. A line for a directory, such as
   `skipped vendor/: 312 changed files in a skipped directory`, counts
   changed files of vendored or built code, which the readers leave out as
   well.

2. Run `scripts/change_parts.py` under the base directory with `python3`
   over `<base>...HEAD`. It prints the parts of the change, about 300 changed
   lines each. Then call `kt:read <base>...HEAD <part>` once for each
   part, with the range and the part number and no other word. The calls may
   run side by side. Save the answers verbatim in the order of the parts. A
   reader that gets a large change whole spreads its attention thin and
   reports little toward its end.
3. Note the head with `git rev-parse HEAD` before you close the first stop.
   Close every stop of the answers. Test the four ways in this order, and use
   the first that answers the question:
   1. a rename or a restructuring that answers the question
   2. a comment written from evidence you can name
   3. a question to the owner
   4. a decline with its reason, when the question asks what the language
      or its standard library does, when the line already answers it, or,
      held to the owner's lines, when the change does not touch the line

   Rewrite or delete a comment that the reader said told it nothing or
   repeated its code. Rewrite each sentence of a `plain` row from what the
   code does, and explain the term of each `term` row where it first
   appears. Check a statement that the reader believed false
   against the code, and correct the statement or the code.

4. When step 3 changed a comment, a document or the code, run a second
   round. In it, list the parts of `<head>...HEAD` with the head you noted in
   step 3, and call `kt:read <head>...HEAD <part>` for each part as in
   step 2, so that the new readers read what step 3 changed. Save their
   answers and close their stops as in step 3. No third round follows.
5. Run `kt:audit <base>...HEAD plan: <plan>` when the change has a
   plan, and `kt:audit <base>...HEAD` when it has none. Held to the
   owner's lines, the word `lines` follows the range. Where the plan names a
   document that the change did not change, such as the local note, its
   path follows `also:`. Save the report verbatim. Apply
   each row, or decline it with its reason. A row that rewrites lines outside
   the change applies only to a block the owner wrote.
6. Run the step check again, fix each finding, and repeat until its last line
   reports 0 findings.

A question to the owner from steps 3 to 5 is asked before the commit that
needs the answer. Ask the owner the way the owner's instructions say, and end
your turn until the answer comes; where they say nothing, ask in this
conversation. A comment that waits for an answer is written after it arrives.

## What the reviewer sees

The review's "Checks" shows the findings of the attack and the rows of the
code audit and the tests audit, each with how it was closed. It shows the last line of each step check, each
`skipped` line, every stop with its closure, every decline with its reason,
each finding left in a block of another author, and the rows of the audit as
applied or declined. Each stop gets one of these lines:

```
<path>:<line> | rename <sha>
<path>:<line> | comment <sha>
<path>:<line> | question
<path>:<line> | decline: <reason>
```

A check counts as run only when its saved answer exists. A session that
reports a check without the saved answer reports a check that did not run.

## Examples

Correct: the session lists two parts of `main...HEAD`, runs
`kt:read main...HEAD 1` and `kt:read main...HEAD 2`, saves the
answers with twelve stops, renames one variable, writes nine notes from the
code and the tests, asks the owner about a constant, and declines one stop
because the standard library defines the term. The reader of the second round
finds one note that told it nothing, and the session rewrites it. The audit
proposes four rows, and the session applies three and declines one with its
reason.

Correct, held to the owner's lines: the step check runs with `--lines` and
prints `skipped CMakeLists.txt: no comment syntax known for .txt`, which the
review lists. A reader stops at a line of a function that the change did not
touch, and the session declines the stop as outside the change. The change
adds a sentence to a walkthrough item that another author wrote, and the
audit proposes to rewrite the whole walkthrough. The session keeps its own
sentence and the rest of the block as they are, and the review lists the
row as a finding left in a block of another author.

Incorrect: the session reads its own comments again and reports that it
found no gaps. It already knows what each line does, so it cannot see where
a reader stops. Or the session adds a hint to the call, such as
`kt:read main...HEAD 1 the parser is the risky part`. A hint tells the
reader what the author knows, and `kt:read` passes the range and the
part number alone to the reader. Or the session asks a subagent to write the
missing comments. The subagent does not know the reasons, so it writes
paraphrases and guesses.
