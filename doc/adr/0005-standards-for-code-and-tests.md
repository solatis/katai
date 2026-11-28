# 0005. Code and tests have standards, and a test's kind is what it touches

Date: 2026-11-28

## Context

Record 0004 gives every standard one frame. This record is about what the
two new rule files say and how they are made to hold.

Without a standard for tests, a plan said "tests are designed the same way"
and left the kind of each test to the build. Two defects followed. A build
wrote tests named integration tests that built the program and started it
from the test framework, although the component was reachable in the test
process. Another wrote a unit test against a hand-written fake for each
function that only forwarded a call. Both passed every check katai had.

Rules that existed only as prose in a repository drifted, and rules that a
lint or a script carried held.

## Decision

`tests.md` draws the kinds of test by what a test touches. A unit test
touches nothing outside the test process. An integration test drives a
component in the test process with its real dependencies, and it starts no
process of the program under test. An end-to-end test is the only kind that
starts the program, and it lives apart. A behavior is tested at the lowest
kind that reaches it. The kinds a repository has are its own decision, and
the first test of a kind is a proposal the owner rules on.

A fake of a subsystem is a Rationale row of the plan. A behavior that holds
for a set of inputs gets a property test. Glue gets no unit test.

`code.md` gives the shape of code in any language: a function computes from
its arguments, input and output sit at the edges, a value is checked once
where it enters, and an interface exists for implementations the tree has. A
rule that a linter can check belongs in the repository's lint and not in a
sentence.

A rule enters either file only if a reader can point at the line that breaks
it. Both files state kinds and no quantities.

Three checks carry the two standards:

1. The plan has a Tests part. Each test sketch names its kind, what it pins,
   why it has its level and its fakes, and `check_steps.py --plan` checks
   that form.
2. The plan stage audits each plan against `code.md` and `tests.md` before
   any code exists.
3. The build stage audits the built change against both, before the checks
   of comments, because the rows of these audits change code.

How a language spells a rule, such as the library that draws inputs, is read
from the tree. The facts of one repository, such as how a live system
reaches a test, stay in its instruction files, and the seed gathers them
with their sources.

## Rejected alternatives

- Kinds drawn by speed or by size. Neither says whether a test may start the
  program, which is the defect the kinds are there to stop.
- A count or a share, such as a share of property tests or a length limit
  for a function. A quantity is met by code that misses the point, and
  record 0002 dropped the last one for comments.
- A language binding in katai, such as one property library per language.
  The tree already shows it, and a list in katai would go stale.
- The audit of code and tests in the same run as the audit of comments. One
  run would read every rule file, and its rows would be harder to close.
- The tests standard before the code standard. A test is code, and the rule
  that sets a fake apart from an interface needs both files.

## Consequences

A plan without a Tests part fails its step check, so a plan written before
this record needs the part, or the word "none", before it is checked again.

A build runs two more audits, and a plan stage two. Each reads one or two
rule files and the lines of one change.

The form check cannot tell whether a named kind is the right one. That is
for the audits, the attack of record 0006 and the owner.
