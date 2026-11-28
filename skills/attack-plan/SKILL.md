---
name: attack-plan
description: Attacks the decisions of one plan before any code exists, and returns each claim of the plan it broke with the case that breaks it. The plan stage runs it, and it changes no file.
context: fork
agent: kt:attacker
background: false
user-invocable: false
argument-hint: "<path of the plan>"
allowed-tools: Bash(true)
---

# Attack a plan

The plan is `$0`. You attack its decisions, before any code is written.

## What you open

- The plan, whole.
- The tree as it is today: the files the plan names, what they use and
  what uses them, and the tests beside them.
- The instruction files and the decision records the plan cites, so that
  you know which limits the author accepted.

You open no rule file of the standards, no other plan and no seed report.

## The claims

1. The Outcome: each thing it says is true when the issue is merged.
2. Each Rationale row: that its decision reaches the Outcome, and that the
   alternative it rejects is worse for the reason it gives.
3. Each sketch of the Design: its contract claims.
4. Each entry of the Tests part: that the test pins what its `pins:` line
   says, and that its `level:` line holds.

## What you look for

- A simpler design that reaches the Outcome and that no Rationale row
  rejects. Name what the tree already has that it would use.
- A case the Design does not handle: a state, an order of events, an input
  or a dependency that fails. Follow it through the sketches and through
  the code of today that they call.
- Something in the tree that the plan duplicates or contradicts, at its
  `path:line`.
- A behavior of the Outcome that no entry of the Tests part pins. Name a
  defect in that behavior that every sketched test would pass.
- An entry of the Tests part whose behavior a lower kind reaches, with the
  interface in the tree that reaches it.
- A commit of the Commits section that assumes what no earlier commit
  delivers.

A row owned by the owner in the Rationale ("Settled by" names the owner
and a date) is a limit the author accepted. You do not reopen it, and a
case that it does not cover is a finding.

## What you report

The first line repeats your arguments. Then one row per finding:

```
<plan line> | <the claim, in a few words> | <the case, exact enough to try> | <path:line in the tree, where the case rests on one>
```

Then, under "Held", one line per claim you could not break, with what you
tried against it. Then, under "Not read", what a case depended on and you
could not open. A plan with no finding still lists what held.
