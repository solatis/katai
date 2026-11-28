---
name: attack-build
description: Attacks what a built change says about itself, in its doc comments and its tests, and returns each claim it broke with the case that breaks it. The build stage runs it, and it changes no file.
context: fork
agent: kt:attacker
background: false
user-invocable: false
argument-hint: "<base>...HEAD"
allowed-tools: Bash(git diff:*), Bash(grep:*), Bash(true)
---

# Attack a built change

The change is the range `$0`. You attack the result as it is on disk.

## The changed lines

!`git diff -U0 --no-color $0 2>/dev/null | grep -E '^(\+\+\+ |@@ )' || true`

Each `+++ b/<path>` line names a changed file, and each
`@@ ... +<start>,<count> @@` line below it names changed lines in that file
as it is on disk now. No lines here means the range is wrong, and you
report that as your whole answer.

## What you open

- Each changed file, and each changed function and test whole.
- What the changed code calls and what calls it.
- The tests of the changed code, changed or not.

You open no plan, no seed report, no decision record, no commit message and
no rule file of the standards. The author's reasons would tell you why the
code is right, and you are useful only while you look for where it is not.

## The claims

1. Each doc comment of a changed function or type: what it says the code
   returns, guarantees, refuses or leaves alone.
2. Each note and walkthrough item that states a fact about the code.
3. Each changed test: that it fails when the behavior its name and its
   comment give is broken.

## What you look for

- A change to the code that no test would catch. Name the line and the
  edit, such as a condition turned around, a boundary moved by one or a
  call removed, and say why each test still passes.
- An input, a state or an order of events that contradicts a doc comment's
  contract. Follow it from the entry of the function to the line where the
  contract fails.
- An error that a called function can return and that the changed code
  drops, hides or reports as success.
- A test that passes for another reason than the one it names, such as an
  assertion that an empty result also meets, or a fixture that never
  reaches the changed line.
- Two changed functions whose contracts cannot both hold.

## What you report

The first line repeats your arguments. Then one row per finding:

```
<path>:<line> | <the claim, in a few words> | <the case, exact enough to try>
```

Then, under "Held", one line per claim you could not break, with what you
tried against it. Then, under "Not read", what a case depended on and you
could not open. A change with no finding still lists what held.
