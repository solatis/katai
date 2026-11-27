# Report, then stop

Reply with exactly these sections, in this order. Every value, candidate,
decision and code claim carries its source, for example `merge:`,
`doc/architecture.md` or `src/sync.rs:42-46`; a claim without a source is
not made. Do not summarize the documents; report only what the unit must
honor. The plan stage may run in a cleared session or another checkout and
reads this report from disk as its whole input, so the report says
everything the plans need.

Each section is a markdown heading, `# Name`, on a line of its own with a
blank line before and after it. Sections carry no numbers. A numbered list
appears only where a section asks for one, and it starts at 1. The
Candidates section belongs to `/katai:start-next` only; when its step did
not run in this seed, it is omitted, not written as "none".

- `# Where` -- first, one line naming the unit's slug, which names this
  report and fills the plans' `Unit:` line. Then one line per value the unit
  rests on (`context.md`, "The values the unit rests on"), with its source:
  a printed line, an instruction file at `path:line`, the skill that
  supplied it, or `settled by owner, <date>` for a value asked once. The
  milestone this seed closed, if any, is a line here with its evidence. A
  line names which skill took each step so far, or says that none did.
- `# Candidates` (`/katai:start-next` only) -- a table, one row per
  candidate, in the order they were offered:
  `| candidate | source (path or item) | tree check (landed / blocked / ready / not read) | verdict |`
  A candidate that the owner did not pick from a list of existing items is
  `not read`.
- `# Brief` -- prose for the owner to read, at most 200 words, no tables,
  no paths: the one section whose claims the sections below evidence
  instead of carrying paths themselves. Three paragraphs: what the unit is
  and what is true when its issues are merged; how it will be done, the
  approach and the shape of the change in plain words; how it fits the
  milestone's goals where there is one and what is in flight, why it comes
  now, and what it leaves for later. Written for a reader who has not
  opened the sources.
- `# Issues` -- one block per issue, in landing order:

  ```
  <n>. <Item title>   (<item> existing, or "new", or "no item")
       slug: <slug>   branch: <branch>   base: <base> | <branch it stacks on>
       PR title: <PR title>
       <one line: what the issue delivers>
  ```

  Each branch name was checked free in this clone and on origin, as
  `katai:workflow`, "Names", says. Where a name carries the key of an item
  that does not exist yet, the key's place stays open.

- `# Decisions` -- a numbered list, one entry per design choice and per
  constraint from Shape each issue, one to three lines each: the issues it
  applies to, the choice or the constraint, the alternative it beats where
  there is one, the reason, its provenance (owner, tree or agent), and
  `settled by <path>` (an `owner` or `tree` source), `settled by owner,
<date>` (the challenge round) or `proposal`. Write "none" if the unit
  leaves no choice to make.
- `# Code involved` -- one line per file, package or directory in the
  scoped set: the path, with `path:line` for each function the unit
  changes, then what it does and how the unit touches it. A plan stage in a
  cleared session reads this in place of the context load, so it names every
  file a plan will name.
- `# Open questions` -- a numbered list of everything the unit's items or
  sources contradict or leave open, every stale entry or gap the survey
  found, every choice Shape each issue found was not yours to make, every
  question the owner deferred, and one line per kind of leftover, with its
  count and its names. Ask; do not resolve by assumption. Write "none" if
  there are none.
- `# Proposed commits` -- per issue, under its slug, numbered one-line
  commit subjects in `type(scope): subject` form, in the order you would
  land them: the outline the plan will refine, so that the owner can
  redirect before the plans are written. Each list closes with its Verify
  step, which is not counted as a commit.

A Where section, for example:

```
unit: upload-retries
checkout: linked worktree, main checkout /src/widget -- checkout:
instruction file: the local note, owner shared -- owner:
base: main -- base:
merge style: squash -- merge: squash 28, fast-forward 0, merge commit 2 (of 30)
names: branch ab-<n>/<slug>, PR title "AB-<n> - <title>" -- recent: #812, #809, #806
tracker: AB keys, no skill covers it; the owner makes each item, settled by owner, 2026-03-02
checks per commit: make fmt -- AGENTS.md:14
CI: github-actions, ci.yml -- ci:
release-2.x: never, settled by owner, 2026-03-02
reviewer: none, settled by owner, 2026-03-02
```

## The two writes

1. The seed report. Write the same text that you reply with to
   `<plans>/<unit>-seed.md`, where `<plans>` is the folder the `plans:` line
   names and `<unit>` the unit's slug. Create the folder with `mkdir -p`
   where it does not exist yet.
2. The orientation, only on the first unit in a shared repository: where
   `owner: shared` and the stage printed `local note: none`. Write the
   orientation that `context.md` gathered to
   `<main checkout>/.claude/AGENTS.md`, where the main checkout is the path
   the `checkout:` line names, also when this session runs in a linked
   worktree. Put it under a heading `## Orientation`, in plain sentences,
   one fact each, each with the path it comes from. It holds nothing about
   the unit and none of the values asked once, which the plan stage
   writes. Then add the line `.claude/AGENTS.md` to
   `<main checkout>/.git/info/exclude`, unless that file already has it, so
   that `git status` stays clean in the checkout and in its worktrees.

Nothing else is written.

Correct: the brief says the server stamps the receive time on each event
before it appends the event to the log, so a client with a wrong clock
cannot reorder the log. It names trusting the client's timestamp as the
alternative and says why it lost, and the decision entry repeats the choice
with what settles it.

Incorrect: the brief says "add event ingestion, 2 issues, 11 commits", and
the owner learns what ingestion does from the commit subjects. Or: the
session runs in a linked worktree, and the orientation goes to the
worktree's own `.claude/AGENTS.md`, where no later stage reads it.

Then wait. The owner opens the plan stage with `/katai:plan`; nothing else
does.
