---
name: start-next
description: Start the next unit of work -- find the candidates, from the active milestone's gap where the repository has open milestones and else from the work in flight, a work list the instruction files name and the owner's unstarted items, ask the owner which of them form the unit, then load their context, put their design choices to the owner and write the seed report without starting the work.
disable-model-invocation: true
allowed-tools: Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/repo_state.py")
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/repo_state.py"`

# /katai:start-next -- seed the next unit, chosen with the owner

Load `katai:workflow` with the Skill tool before anything else. The lines
above are what the stage printed; read them as its "What the stage printed"
says. Where they hold `no repository of its own`, `no main checkout (bare)`
or `no GitHub origin`, say so and stop.

This skill takes no argument. You find the candidates, let the owner choose
which of them form the unit, and then seed that unit exactly as
`/katai:start` would have, had the owner named those items or described
that work.

## This turn

Read and report. The seed writes two things: the seed report, and on the
first unit in a shared repository the orientation in the local note. The
one other write is closing a met milestone, where `milestones.md` allows
it. You write no code, documents or plans, create no tracker items or
branches, make no commits and delete nothing.

## Steps

1. Detect, from the printed lines: what is in flight and the leftovers, as
   `katai:workflow`, "In flight and leftovers", defines them. Each kind of
   leftover is one line with its count and its names, for the report's
   Open questions.
2. Find the candidates. A sentence of the instruction files or of the local
   note that says where this repository's candidates come from, or which
   items are never offered, decides before the two cases below.
   - Where `milestones:` shows one open milestone or more, read
     `${CLAUDE_SKILL_DIR}/milestones.md` whole and follow it. Its
     candidates are cut from the milestone's goals.
   - Otherwise the candidates are existing items: the work in flight here,
     then the next items of a work list the instruction files name, then
     the owner's unstarted items that name this repository, through the
     skill that covers the tracker. If a skill in this session covers this
     repository's tracker, use it for this step. The stage keeps the order
     of the steps and the gates; the skill supplies how the step is done.
     Where no skill covers it, the tracker evidence decides, as
     `katai:workflow`, "Units and issues", reads it. With GitHub issues, the
     owner's unstarted items are the open issues assigned to the owner
     (`gh issue list --state open --assignee @me --json number,title,milestone`)
     that no plan and no open pull request names. With another tracker's
     keys and no skill, those items cannot be read: say so in the question.
     With no tracker, there are none.
3. Prepare the candidates for the question.
   - Candidates cut from goals: load `katai:seed` with the Skill tool, with
     the candidates that are not in flight as the unit, and run its context
     step only. Return here before shaping anything. Then Check and cut,
     below.
   - Existing items: Triage, below. Do not load `katai:seed`, and read no
     code, before the owner has picked.
4. Ask, below. The owner's pick is the unit.
5. For picked work in flight: one line per issue with its stage and the
   next command, from the table in `katai:workflow`, "In flight and
   leftovers", before anything else in the reply. Where the pick holds
   nothing else, that is the whole reply, and nothing opens a stage. For
   the rest of the pick, where step 3 ran the context step: the rest of
   `katai:seed`, that is the shape, the challenge round, the report and the
   wait for `/katai:plan`. Where step 3 did not: load `katai:seed` with the
   Skill tool, with the pick as the unit, and run all of it, as
   `/katai:start` does for the items or the work the owner names. The
   report's Candidates section is present, because steps 2 and 4 ran.

With no candidate at all, ask the owner what to work on. The answer is a
description, and you seed it as `/katai:start` seeds one.

Name in the report's Where which skill read the tracker, or that none did.

## Check and cut

This is for candidates cut from goals. They share the milestone's context,
and how they are cut is what the owner chooses between, so the context step
runs for all of them before the question.

Check each candidate against the tree, not against its description. Has it
already landed? Are the things it builds on present, or in another
candidate? Does it need the owner's hands or an outside party rather than
commits? A candidate the tree shows as landed is stale: report it, and do
not offer it.

A candidate is offered as an issue only when it is right-sized: one
subject; mergeable on its own, so that the base builds and passes lint and
tests after it lands; exercised by a test or a command that exists when it
lands. The size of an issue is the length of its commit list, so first
write each candidate's whole commit list, at the granularity
`katai:workflow`, "Branches and commits", prescribes, from the context step.
A candidate too large to review as one change is split into issues at the
points where the base stays green. A small candidate is offered as it is,
or folded into a candidate on the same subject where the owner would review
the two as one change anyway.

The label of such a choice is the issue in a few words and its commit count.
The description says, in two or three sentences, what the owner will have
to review: the directories and files touched, whether the code is new or
edited, how much of it is library code, tests, fixtures or documents, and
what it depends on, "stacks on <other choice>" where it needs that choice's
code and "independent" otherwise. Recommend a set that shares context, so
that one context load and one challenge round serve all of it, and whose
commits total about 15 or fewer, so that the review is one sitting; a set
that runs over says so.

## Triage

This is for existing items. Each is on a subject of its own, so the context
of one serves no other: reading the tree for every candidate costs one
context load per candidate, and the owner picks one or two. So the seed
reads the tree for the pick, and nothing reads it before.

Triage from what the listing printed: each item's key, its title and what
else the listing shows, such as a label, a milestone or a parent item. Read
an item's body only where its title does not say what the item asks for.
Read no code, no document and no source outside the repository. The one
read of the tree is a search, of the files or of `git log`, for a name that
a title gives, where the title reads as work that may have landed. A
candidate that this search shows as landed, or whose title or body places
its work in another repository, is reported in one line and not offered.
Whether an offered item is blocked, and how large it is, the seed finds for
the pick.

The label of such a choice is the item's key and its title in a few words,
with no commit count. The description is one sentence: what the item asks
for, in plain words. Recommend the first candidate in the order they were
found, or a set whose titles share a subject, with that as the reason.

## Ask

Ask the owner the way the owner's instructions say, and end your turn until
the answer comes; where they say nothing, ask in this conversation. Ask one
question in which the owner may pick several choices, at most four: work in
flight first, then the candidates in the order they were found. Each choice
has a label and a description, as Check and cut or Triage says. A choice
for work in flight names its stage and its next command instead. After the
choices, a line of its own names the set you recommend doing together, with
its reason. Candidates beyond the four choices are named in one line before
the question, each by its key and title, so that the owner can pick one in
words.

The owner's pick is the unit. The candidates the pick leaves are listed in
the report's Candidates section, and no item is made for them.

An answer may correct the candidates instead of picking: it says where this
repository's candidates come from, or which items are never offered, such
as "only the items of the current release" or "the list is `TODO.md`, not
the tracker". Take the candidates again as the answer says, and ask again.
The answer is a value of the repository: the report's Where carries it as
`candidates: <the answer>, settled by owner, <date>`, and the plan stage
writes it into the instruction file with the values asked once, so that the
next run starts from it. Ask for no such sentence where the owner gave
none.

Correct: the milestone's goal is "a command line tool that scripts can
drive". The tree has the tool's commands, and they print only text. You cut
four candidates: JSON output, 5 commits, independent; stable exit codes, 4
commits, stacking on JSON output because it reuses its error type; a config
file loader, 7 commits, independent; shell completion, 3 commits,
independent. You recommend JSON output and exit codes together, 9 commits,
one error type to review. The owner picks those two, and the report lists
the other two as candidates.

Incorrect: the whole goal offered as one choice of 23 commits; or four
choices that differ in commit granularity rather than in subject; or
descriptions that give a commit count and nothing about the code; or the
four candidates made into items before the owner chose.

Correct: the repository has no open milestone, and the listing prints seven
of the owner's unstarted items. One title names a flag, and `git log` shows
the commit that added it: that item is reported as landed and not offered.
You offer the first four of the other six by key and title, name the last
two in a line before the question and recommend the first. The owner picks
the second, and the seed loads the context of that one item.

Incorrect: the same seven items, and before asking you read the code and
the release notes of a dependency for each of them, to write seven commit
lists, of which the owner picks one.
