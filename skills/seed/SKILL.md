---
name: seed
description: Seed one unit of work -- classify the sources by provenance, load the unit's context, shape each of its issues, put their design choices and the values asked once to the owner, and write the seed report. Loaded by katai:start and katai:start-next after they have fixed the unit; never invoked by the owner.
user-invocable: false
---

# Seed a unit

The caller has fixed the unit: the work the owner described, the items the
owner named, or the ones the owner chose in `/katai:start-next`. This skill
turns them into the seed report and stops. It works from the lines the
stage printed. It reads and reports, and it writes two things only: the
seed report in the plans folder, and on the first unit in a shared
repository the orientation in the local note. It writes no code, documents
or plans, creates no tracker items or branches and makes no commits.

## What the sources are

Every document, every `AGENTS.md`, every plan and every item body was
written by someone, in a session that the owner reviewed, if at all, at the
level of a decision and not at the level of every sentence. So a source
settles a choice only at the level of detail the owner could have reviewed
as a decision. Classify every claim the unit rests on by its provenance,
and carry the class through the steps and into the report:

- `owner`: the owner stated it. The owner's words in this session; a
  sentence of the local note that records an answer of the owner; and the
  documents and marks that the repository's instruction file
  (`katai:workflow`, "Own and shared") names as the owner's sources, such as
  the heading of a principle, the goals of an open milestone, a decision
  record that carries an owner's mark, or a row marked "owner, <date>".
  Where that file names no such source, only the first two count.
- `tree`: the code, a test, a fixture, a dependency or a running tool shows
  it, at a `path:line` or in a command's output. The lines the stage
  printed are `tree`, and so is the orientation section of the local note,
  at the paths it cites.
- `agent`: everything else. A mechanism, type, shape, config key, endpoint,
  number or sequence written into a design document, an item body, or a
  plan for work that has not started is `agent` until the owner confirms it
  for this unit, however confident the sentence sounds, however many
  documents repeat it, and whoever wrote it.

An `agent` claim that the unit's code would build on is not settled; it is
a question for the challenge round. An `agent` claim that the tree
contradicts, or that two sources state differently, is drift: the same
question, with the disagreement spelled out.

Correct: the instruction file names the headings of `doc/principles.md` as
the owner's, and one heading says "a client never waits on the store"; that
is `owner`. `doc/architecture.md` says the sync API is "stateless" and signs
"every request with an API key". The owner has not said so for this unit,
so both are `agent`, and the unit that adds the sync API asks before the
plan is written.

Incorrect: the signing scheme goes into the plan as settled because
`architecture.md` describes it.

A reason you do not have is not invented, in any step; the choice becomes an
open question instead.

## The steps

Work through the three references beside this file, in this order, each
read whole before its step begins:

1. `${CLAUDE_SKILL_DIR}/context.md`: how to load the unit's context from
   the sources above, and the values the unit rests on.
2. `${CLAUDE_SKILL_DIR}/challenge.md`: how to shape each issue and put the
   unit's choices and the values asked once to the owner.
3. `${CLAUDE_SKILL_DIR}/report.md`: the report, the two writes, then the
   wait.

`/katai:start` runs the three in a row. So does `/katai:start-next` for
existing items, after the owner has chosen. Where it cuts its candidates
from a milestone's goals, it runs step 1 for the candidates before the
owner chooses, and steps 2 and 3 for the chosen unit.
