# Shape each issue

The report explains the unit to the owner before it lists anything, so
settle its shape before writing. From what you read, decide for each issue:

1. The outcome: what is true in the tree when the issue is merged, and what
   it leaves for later.
2. The approach: the shape of the change, where it lives, what it reuses,
   what it introduces.
3. Its base: the repository's base, or the issue whose code it needs, which
   makes it a stacked branch on that issue's branch. Stack only when the
   code needs the other issue's commits, or when the owner would never merge
   one without the other; an independent issue can merge alone.
4. Each design choice it requires: the option you take, the alternative it
   beats, the reason, and what settles it. A choice an `owner` source
   settles carries that path. A choice that only `agent` sources settle, or
   that the sources leave open, goes to the owner in the challenge round
   below. What the owner answers is settled by the owner. What the owner
   leaves to you is a proposal: you still pick, you say that the pick is
   yours, and the approval of the plan review settles it. A choice that
   contradicts a settled decision, or that would make an issue materially
   different work, is not yours to make; it goes under Open questions.
5. Each constraint it must honor: a settled decision, a rule of the
   instruction files, or a gotcha of the tree, with its path and its
   provenance. The report folds each into a decision.

A choice two issues share, such as one error type for two commands, is
settled once, for the unit, and both issues carry it.

# Challenge round

The plans are written after this report, and they carry the approach the
owner wants, not the approach the documents happen to record. So before the
report, put the choices to the owner, while the context is loaded and
nothing is written.

What gets a question. A choice an issue's code rests on that is:

1. `agent` by provenance, including every detail of a design document that
   the unit would be the first to implement;
2. drift between sources, or between a source and the tree;
3. expensive to reverse once code exists: a wire shape, a public signature,
   a config key, a storage layout, a dependency, a package boundary;
4. one where a simpler alternative exists and no source records why it
   lost.

What gets no question: a choice marked `owner`; a choice the tree settles;
a choice that belongs to a later issue; a choice between wordings. A
question whose answer would not change a commit of this unit is not asked.

## The values asked once

A value the unit rests on (`context.md`, "The values the unit rests on")
that no printed line, instruction file or covering skill settles is asked
once, here, with history's answer as the recommendation. A
`release candidates:` line, for example, names a branch but does not say
whether it takes merges. Its answer becomes one
plain sentence in the repository's instruction file, a "no" included, so
that no later unit asks it again. The plan stage writes that sentence; this
round only asks. Read the instruction files and the local note first: a
value they give is not asked.

- Each release candidate that the instruction files and the covering skills
  do not name. One question per candidate, with three choices in this
  order: "takes every merge", "only when named at the plan review" and
  "never". History's answer comes from the candidate's count and its last
  date on the `release candidates:` line.
- The checks each commit runs, where the instruction files name no command.
  The recommendation is what CI runs, as the files of the `ci:` line show.
- The reviewer, where neither the instruction files nor the skill that
  covers pull requests names one and the `approvals:` line shows approvers.
  The recommendation is the most frequent approver, and "nobody" is a
  choice. Where the line shows no approver, there is no reviewer and nothing
  is asked.
- How items are made, where `item keys:` shows another tracker's keys and
  no skill in this session covers that tracker. The choices are "the owner
  makes each item and gives its key at the plan stage" and "no item, the
  plan is the item", and the recommendation follows the counts on the
  `item keys:` line.
- A conflict between a rule of the instruction files and a rule file of
  katai's standards (the `standards` folder beside this skill's base
  directory) on the lines the owner's change adds: which rule wins there.
- Any other value a later step needs that nothing gives.

In `/kt:start-next`, `milestones.md` may have asked the order of the
milestones already. That answer is carried into the report like the others
and is not asked again.

## How to ask

Ask the owner the way the owner's instructions say, and end your turn until
the answer comes; where they say nothing, ask in this conversation.

Ask every open question, one question per choice. Group the questions by
subject, one round per subject: the questions of a subject go out together,
and the next round and the report wait for their answers. The values asked
once are a subject of their own.

The owner reads the question cold: the context you loaded is not in front
of them, and a name from the code means nothing until the question says
what it is. So the question text carries the context, in this order, before
it asks anything: what the thing is and what it does today, in plain words
("a client reads the feed one page at a time, and each answer carries a
cursor the client sends back for the next page"); what the issue changes
about it and why that raises a choice ("this issue adds the first cursor,
and every client stores it, so its form is fixed now"); then the question.
An identifier appears only after the sentence that explains it, in
parentheses, so that the owner can find it in the code. The question runs
three to six sentences; a one-line question is a sign that the context was
left out.

The choices follow the same rule. Each choice is a label in plain words,
not in identifiers ("the last item's id", not "next_cursor() -> u64"),
followed by what it does, what it costs and what it keeps open, naming an
identifier only after saying what it is. The choices are: the approach the
sources record, named by its path; the simplest alternative; a third where
a real one exists. Keep them in that order. After them, on a line of its
own, name the choice you would take and say why in one clause; never list
it first and never put the recommendation into its label. The owner can
always answer in words of their own. An answer is the decision; it is not
argued with.

## Where the answers go

Each answer is the owner's decision as of today's date, and the report
carries it as `settled by owner, <date>`: a design answer in its Decisions
entry, and a value in its Where line. The plan's Rationale repeats a design
answer under "settled by" in the same words, so that the build can land it
marked the same way. The plan stage writes each value into the repository's
instruction file; the seed writes none of them. A choice the owner left to
you is `proposal` and keeps your recommendation. An answer that gives an
issue a new direction reshapes it before the report is written: run Shape
each issue again for what the answer touches, and ask what the new shape
raises.

A question the owner defers goes under Open questions. The plan records your
recommendation for it, and the approval of the plan review settles it.

Correct: `doc/architecture.md` says the feed is "paged by a cursor", no
document says what the cursor holds, and the unit adds the first paged
endpoint. The question says: a client reads the feed one page at a time;
each answer carries a cursor that the client sends back for the next page;
this issue adds the first cursor, so its form is fixed for every client
now; the architecture document says only that the feed is paged by a
cursor; should the cursor be the last item's id or an opaque offset? The
owner picks the id; the Decisions entry says `settled by owner, <date>`,
and the plan's Rationale repeats it.

Correct: the `release candidates:` line shows
`release-2.x (9 in 90 days, last <date>)`, and no instruction file names it.
The question says what the branch is and what its count shows, and offers
"takes every merge", "only when named at the plan review" and "never", in
that order, with "takes every merge" recommended after them because 9 of the
base's commits reached it in 90 days. The owner answers "never", and the
Where line says `release-2.x: never, settled by owner, <date>`.

Incorrect: the id is chosen because it sounded right, and the owner learns
the cursor's form from the diff. Or: the question is "Should `next_cursor()`
return `u64` or `String`?", so the owner has to open the code to learn what
the cursor is. Or: three of the questions are about an issue the owner did
not choose. Or: the id is listed first with the recommendation in its
label, so the order says which one you want before the owner has read the
alternatives. Or: the seed writes the answer about `release-2.x` into the
instruction file itself.
