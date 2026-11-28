# 0006. An attacker tries to break the claims of each plan and each built change

Date: 2026-11-28

## Context

The cold reader says whether a change can be read, and the auditor whether
it follows the rules. Neither asks whether what the change says about itself
is true. A function can be readable, follow every rule and still return
success on a failed write, and a test can be of the right kind and still
pass when the behavior it names is broken. A plan can pass its form check
and its audits and still build a type the tree already has.

## Decision

A third agent, `kt:attacker`, assumes each claim is false and looks for the
case that shows it. A finding is a case the author can check without the
attacker: an input, a state, an order of events, a change to the code or a
simpler design. For each claim it could not break it says what it tried, so
that a claim that held can be told from one that was not attacked.

Two skills run on it, because the claims of a plan and of a built change
differ, and so does what the attacker may open:

- `kt:attack-plan` attacks decisions: the Outcome, the Rationale rows, the
  contracts of the sketches and the entries of the Tests part. It reads the
  plan and the tree of today.
- `kt:attack-build` attacks the result: the doc comments and the tests of
  the changed code. It reads no plan, because the author's reasons would
  tell it why the code is right.

Neither reads a rule file. Each runs once and first among the checks of its
stage, because its findings change the most. A finding is closed by a change,
a question to the owner, or a decline that names the line that refutes the
case. The answers are saved as `<slug>-plan-attack.md` and
`<slug>-build-attack.md`, and the reviews show each finding with how it was
closed.

## Rejected alternatives

- One skill that takes a plan or a range. The auditor can do that because
  its rules are the same for both. The attacker's claims, what it opens and
  the form of a finding all differ.
- The attacker's questions as a focus of the auditor. An auditor that cites
  rules reports departures from rules, and a case that breaks a claim breaks
  no rule.
- A build attacker that reads the plan. It would inherit the reasons and
  stop finding what the author missed.
- A second attack after the fixes. The fixes carry their tests, and the
  audits and the readers still read them.
- Adding the attacker only after a unit had been built under records 0004
  and 0005, so that one change is judged at a time. The owner chose to land
  the whole design at once, so the first units judge the three readers
  together.

## Consequences

A plan stage and a build stage each start one more agent run per issue. The
attack reads more of the tree than the other readers, so it costs the most
of them.

The prompts of the attacker rest on no unit built with them. The first
units show whether its findings are cases or opinions, and the examples in
`agents/attacker.md` are the place to correct that.
