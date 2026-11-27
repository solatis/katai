# doc/adr/

Decision records of katai: one file per decision, saying what was decided,
why, what lost and what it costs. A record describes the decision as it stands
today. When a decision changes, its record is rewritten in place. Records are
numbered in the order the decisions were first made, and the number is how a
skill or a comment cites one.

Each record has the same parts: `Date`, then Context, Decision, Rejected
alternatives and Consequences. A part with nothing recorded says so.

A change to a rule of weight in a skill writes or rewrites its record in the
same commit, as "Changing a rule" in `skills/workflow/SKILL.md` asks.

No record is written yet.

| Record | Decision |
| ------ | -------- |
