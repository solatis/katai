# Load context

The `AGENTS.md` hierarchy is the map. The root file says which document
answers which question, and the `AGENTS.md` of a directory says what that
directory is and how to change it. Where the repository has no `AGENTS.md`,
the instruction files Claude Code loaded, the `README` and the layout of the
top folders are the map. In a shared repository the local note, which the
stage printed, is part of the map. Follow that map rather than a list kept
here, so that this skill stays correct as the repository changes.

First, scope. From the unit's issues and the structure of the repository as
its documents describe it, write down the set the unit touches:
directories, packages or modules, endpoints, config blocks, tests,
documents. This set decides what you read below; extend it when reading
reveals a dependency.

Then read, in this order, skipping what the caller's survey already
covered:

1. The items: each existing item's title and body, and the description of
   its milestone where it has one. If a skill in this session covers this
   repository's tracker, use it for this step. The stage keeps the order of
   the steps and the gates; the skill supplies how the step is done. Where
   none does, read a GitHub issue with
   `gh issue view <n> --json number,title,body,state,milestone,comments`.
   An item that neither can read is a question to the owner: its title and
   what it asks for.
2. The documents the map routes the unit's subject to, whole.
3. The `AGENTS.md` of every directory in the scoped set, and of each parent
   directory on the way there.
4. The code in the scoped set and what it depends on, read directly. Find
   it with Grep and Glob from the scoped set. Read the functions the unit
   will touch whole, top to bottom, with their callers, their tests, and the
   parts of each dependency the unit will call. A summary of code, your own
   or a helper's, is a map and not evidence: a claim from it enters the
   report only after you have read it in the tree at a `path:line`.
5. The history of the scoped paths: `git log --oneline -- <paths>`, and the
   diffs of the commits that introduced or last changed the functions the
   unit will touch, so that the unit continues the existing direction
   instead of restarting it.
6. Plans in flight: every plan in the plans folder whose item is still
   open, as the `plan:` lines name them, for work the unit would collide
   with or build on.
7. Memory: any recalled note about this repository that bears on the unit,
   verified against the tree before you rely on it.

When sources disagree, the tree wins over any document for what exists
today, and an `owner` claim wins over an `agent` claim for what should
exist. Between two `agent` claims, or between an `agent` claim and the
unit's description, there is no precedence. Every disagreement is drift,
and drift is a question in the challenge round, with both readings and
their paths. It is not resolved by assumption, nor by picking the newer
document.

Look actively for: settled decisions the unit must honor; a document whose
content moves next to the code the unit creates, where the instruction
files have such a rule; known gaps in the dependencies the unit will call;
what the existing tests and fixtures already pin; and anything in the
unit's description that contradicts a settled decision.

## The values the unit rests on

Every later stage rests on a few values of the repository. The report's
Where section shows each with its source, so that a wrong reading meets the
owner before any plan is written. Gather them now:

- The checkout, main or linked, and `owner:` own or shared, which decides
  the repository's instruction file (`kt:workflow`, "Own and shared").
- The base: the `base:` line, or a base the instruction files name for
  this work.
- The merge style: the `merge:` line.
- The forms of the names: the `recent:` lines, the instruction files, and
  the skill that covers the tracker (`kt:workflow`, "Names").
- The tracker and how items are made: the skill that covers it, or the
  tracker evidence (`kt:workflow`, "Units and issues").
- CI: the `ci:` line, or the skill that covers CI.
- The checks each commit runs (`kt:workflow`, "Branches and commits").
  Under a fast-forward they are the build, lint and test commands the
  instruction files name. Under a squash they are what the instruction
  files name to run for a change, such as a format command or a build of
  the touched code, and that may be nothing at all. Where the instruction
  files name no command, under either style, this value has no source.
- The release lines: each `release candidates:` line, and what the
  instruction files or a covering skill say about it.
- The reviewer: the one the instruction files name, else the one the skill
  that covers pull requests names. Where neither names one, the `approvals:`
  line is history's answer, for the challenge round.
- For each existing item: the item, and the skill that read it.

Each value has a source: a printed line, an instruction file at
`path:line`, or the skill that supplied it. A value that has none of these
is asked once, in the challenge round (`challenge.md`).

## A first unit in a shared repository

Where `owner: shared` and the stage printed `local note: none`, gather as
well what a later stage needs to find its way here: the layout in a few
lines; the build, lint and test commands, with the file that names each;
and the conventions you found, such as the base, the merge style, the forms
of the names and the CI. `report.md` writes this orientation into the local
note.
