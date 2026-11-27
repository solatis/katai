# katai

A staged workflow for Claude Code. A piece of work moves through four stages,
and only your own command opens the next one:

| Command                       | What it does                                                         |
| ----------------------------- | -------------------------------------------------------------------- |
| `/katai:start <task or item>` | reads the repository, shapes the work and puts its choices to you    |
| `/katai:start-next`           | finds the next piece of work in the tracker and starts it            |
| `/katai:plan`                 | writes one plan per issue and shows the plans for your review        |
| `/katai:build`                | lands the commits, runs the comment checks, opens the pull requests  |
| `/katai:merge`                | lands each approved pull request and draws lessons from your reviews |

The name is kata plus AI. katai is also a Japanese word for firm, rigid and
stubborn, which describes an opinionated workflow well.

## Install

katai needs `git`, `gh` and `python3` on the `PATH`.

```sh
git clone https://github.com/solatis/katai.git
claude plugin install katai --marketplace "$PWD/katai"
```

Claude Code then loads katai from that clone. An edit in the clone is what
the next session runs, and a running session takes it after `/reload-plugins`.

katai keeps its plans under `~/.local/state/katai`, outside every checkout, so
that a cleared session and a linked worktree find them. In the default
permission mode Claude Code asks before each read outside the working
directory. To stop that, list the folder under
`permissions.additionalDirectories` in your user settings.

To remove katai:

```sh
claude plugin uninstall katai@katai
claude plugin marketplace remove katai
```

Your plans and the clone stay.

## How katai fits a repository

katai names no tracker product, no reviewer and no company. A stage learns
where it is in three steps:

1. A script reads the repository on every run: its default branch, how pull
   requests are merged, its CI, its release branches, its open work.
2. It reads the instruction files Claude Code loads there, such as
   `AGENTS.md`.
3. It hands a step to your own skills where one covers it. A stage says "create
   the tracker item the way this project does it", and a skill of yours whose
   description covers that tracker takes the step. Without such a skill katai
   uses GitHub issues and milestones where the repository's history shows
   them, and makes no tracker item where it shows no tracker.

What none of the three says, katai asks you once and writes down as a plain
sentence in the repository's instruction file.
