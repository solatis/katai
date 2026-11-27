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

**Status: this repository holds the plugin's frame and its install command.
The skills behind the commands are not in it yet.**

## Install

katai needs `claude`, `git`, `gh` and `python3` on the `PATH`.

```sh
git clone https://github.com/solatis/katai.git
katai/install.sh
```

Claude Code then loads katai from that clone. An edit in the clone is what
the next session runs, and a running session takes it after `/reload-plugins`.

The install command does two things:

- It runs `claude plugin install katai --marketplace <clone>`.
- It adds the clone and `~/.local/state/katai` to
  `permissions.additionalDirectories` in your user settings. katai keeps its
  plans under `~/.local/state/katai`, outside every checkout, so that a
  cleared session and a linked worktree find them.

`katai/install.sh --uninstall` removes both again. It leaves your plans and
the clone alone.

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
   uses GitHub issues and milestones.

What none of the three says, katai asks you once and writes down as a plain
sentence in the repository's instruction file.
