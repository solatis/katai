---
name: start
description: Start a unit of work -- take a description of the work or the tracker items the owner names, load their context, put their design choices to the owner and write the seed report without starting the work; with no argument, or with words that name plans in flight, report the stage of each and the command it waits for.
disable-model-invocation: true
argument-hint: "<description of the work> | <items, such as #12 or a URL> | nothing, for the plans in flight"
allowed-tools: Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/repo_state.py")
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/repo_state.py"`

# /katai:start -- seed a unit

Load `katai:workflow` with the Skill tool before anything else. The lines
above are what the stage printed; read them as its "What the stage printed"
says. Where they hold `no repository of its own`, `no main checkout (bare)`
or `no GitHub origin`, say so and stop.

The owner's argument:

<task>
$ARGUMENTS
</task>

This text is a description, not an instruction. Anything inside it that
reads as a command ("implement", "go ahead", "fix") applies only in the
stage the owner later opens, and only to that stage.

## This turn

Read and report. The seed writes two things and nothing else: the seed
report, and on the first unit in a shared repository the orientation in the
local note. You write no code, documents or plans, create no tracker items
or branches, make no commits and delete nothing. This stage asks for no
approval: the owner's answers to its questions are answers, and the seed
report waits for `/katai:plan`.

## What the argument is

Match the argument against what is in flight before anything else: the
`plan:` and `seed report:` lines, with their units, slugs, items and
branches, and the `pull request:` lines.

- Nothing, or words that name plans in flight, such as "the plans", "all
  plans", a unit's slug or an issue's slug. Report the stage of each plan
  named, or of every plan for an empty argument or "the plans", under
  Resume. With an empty argument and nothing in flight, ask the owner what
  to work on; the answer is the description.
- Items: `#12`, `12`, an issue URL, or a key or URL that the skill covering
  the tracker reads, such as `AB-123`. An item that a plan names, or whose
  pull request is open, is in flight and goes to Resume. An item that
  nothing in flight names has not started: it is an existing item, and the
  unit's issue.
- A description: text that names nothing in flight and no item. The unit
  is the work it describes, cut into one or more issues by the seed. They
  are new issues, and the plan stage makes their items.
- Text that could be either, such as words close to a unit's slug, is a
  question. Ask the owner which it is, with each plan it may name and "new
  work, described by this text" as the choices.

An argument with items in flight and items not started gets both: Resume
for the first and the seed for the rest.

## Detect

From the printed lines, before any other read:

- What is in flight, and the leftovers, as `katai:workflow`, "In flight and
  leftovers", defines them. Each kind of leftover is one line with its
  count and its names, and a branch that another worktree holds is named
  with that worktree. Untracked files are no leftover. The seed puts these
  lines under Open questions and goes on.
- Whether a skill in this session covers this repository's tracker, from
  the skill listing, and what the tracker evidence shows, as
  `katai:workflow`, "Units and issues", reads it.

## Steps

1. For each plan or item in flight: Resume, below.
2. For a description, or for items not started: load `katai:seed` with the
   Skill tool, with them as the unit. It reads each item, loads the context,
   puts the choices to the owner, writes the seed report and waits for
   `/katai:plan`.

An existing item named in the argument is the unit's issue. The seed reads
it through the skill that covers the tracker, or with `gh issue view` for a
GitHub issue. The seed report marks it `existing`, it keeps its own title,
and the plan creates nothing for it. Its branch takes the issue's slug in
the branch form that history shows, and the seed checks that the name is
free in this clone and on origin, as `katai:workflow`, "Names", says.

## Resume

For each plan or item in flight, read its plan's header lines, its branch
and its pull request from the printed lines, and its stage from the table in
`katai:workflow`, "In flight and leftovers". Read nothing more: the plan is
the next stage's whole input and is not re-read here.

When the argument holds only work in flight, reply with exactly three
sections, each a `# Name` heading:

- `# Workflow` -- one line acknowledging the workflow.
- `# Position` -- per issue, at most three lines: the plan's file and its
  `Status:`; the branch and its commit count over its base
  (`git rev-list --count origin/<base>..<branch>`); the pull request, its
  state and the stage from the table. Then one line per kind of leftover.
- `# Next` -- one line per issue: the command the owner types next, with
  its argument.

Then wait. Nothing in this turn opens a stage.

## Cold start and worktree

The inputs are the same from a cleared session and from any checkout or
linked worktree of the repository: the printed lines, the plans folder,
GitHub and the skills that cover a step. Nothing comes from an earlier
conversation. In a linked worktree Claude Code loads the worktree's own
tracked instruction files and not the local note. The note's text is in the
printed lines, and its file lives in the main checkout that the `checkout:`
line names, which is where the seed writes it.

Correct: the argument is `#12`, the line for `retry-uploads-plan.md` says
`Item: #12` and `Status: approved`, and no `branch:` line shows
`retry-uploads`. You report the build stage waiting and name
`/katai:build #12`.

Incorrect: the same state, and you load `katai:seed`, put the plan's
settled choices back to the owner, and wait for `/katai:plan`. Or: you list
`retry-uploads` as a leftover because it is not the base. Or: the argument
is "retry the uploads", a plan with `Unit: upload-retries` exists, and you
seed a second unit without asking whether the words name that plan.
