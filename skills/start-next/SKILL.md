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
2. Find the candidates.
   - Where `milestones:` shows one open milestone or more, read
     `${CLAUDE_SKILL_DIR}/milestones.md` whole and follow it.
   - Otherwise: Show the work in flight here, then the next items of a work
     list the instruction files name, then the owner's unstarted items that
     name this repository, through the skill that covers the tracker, then
     ask the owner which to take. If a skill in this session covers this
     repository's tracker, use it for this step. The stage keeps the order
     of the steps and the gates; the skill supplies how the step is done.
     Where no skill covers it, the tracker evidence decides, as
     `katai:workflow`, "Units and issues", reads it. With GitHub issues, the
     owner's unstarted items are the open issues assigned to the owner
     (`gh issue list --state open --assignee @me --json number,title,milestone`)
     that no plan and no open pull request names. With another tracker's
     keys and no skill, those items cannot be read: say so in the question.
     With no tracker, there are none. Steps 3 and 4 are how the owner is
     asked.
3. Load `katai:seed` with the Skill tool, with the candidates that are not
   in flight as the unit, and run its context step only. Return here before
   shaping anything.
4. Check, cut and ask, below. The owner's pick is the unit.
5. For picked work in flight: one line per issue with its stage and the
   next command, from the table in `katai:workflow`, "In flight and
   leftovers", before anything else in the reply. Where the pick holds
   nothing else, that is the whole reply, and nothing opens a stage. For
   the rest of the pick: the rest of `katai:seed`, that is the shape, the
   challenge round, the report and the wait for `/katai:plan`. The report's
   Candidates section is present, because steps 2 and 4 ran.

With no candidate at all, ask the owner what to work on. The answer is a
description, and you seed it as `/katai:start` seeds one.

Name in the report's Where which skill read the tracker, or that none did.

## Check, cut and ask

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

Ask the owner the way the owner's instructions say, and end your turn until
the answer comes; where they say nothing, ask in this conversation. Ask one
question in which the owner may pick several choices, at most four: work in
flight first, then the candidates in the order they were found. After the
choices, a line of its own names the set you recommend doing together, with
its reason. Recommend a set that shares context, so that one context load
and one challenge round serve all of it, and whose commits total about 15 or
fewer, so that the review is one sitting; a set that runs over says so.

Each choice has a label and a description. The label is the issue in a few
words and its commit count. The description says, in two or three
sentences, what the owner will have to review: the directories and files
touched, whether the code is new or edited, how much of it is library code,
tests, fixtures or documents, and what it depends on, "stacks on <other
choice>" where it needs that choice's code and "independent" otherwise. A
choice for work in flight names its stage and its next command instead. The
owner's pick is the unit. The candidates the pick leaves are listed in the
report's Candidates section, and no item is made for them.

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
