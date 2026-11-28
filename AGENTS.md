# katai

katai is a Claude Code plugin that carries a staged workflow into any
repository. `README.md` says what it does for a user. This file is for agents
that change katai itself.

## Layout

- `.claude-plugin/plugin.json` names the plugin. Its skills are typed
  `/kt:<skill>`.
- `.claude-plugin/marketplace.json` lists the plugin with `source: "./"`, so
  that `claude plugin install kt --marketplace <clone>` installs it from a
  clone and loads it from there.
- `skills/` holds one folder per skill. `start`, `start-next`, `plan`, `build`
  and `merge` are the commands the owner types. `workflow`, `seed`,
  `postmortem`, `standards`, `read` and `audit` are loaded by
  those and never typed.
- `skills/workflow/SKILL.md` holds what every stage shares. The "Changing a
  rule" section of `skills/workflow/rule-changes.md` beside it holds for
  every change to a skill here.
- `agents/` holds one read-only agent per stance. `read` runs on
  `cold-reader.md`, which knows no rule and reports where it stops. `audit`
  runs on `auditor.md`, which holds each line against a rule. An agent
  file says how its reader thinks, and a skill says what is read and how
  the answer is formed.
- `skills/standards/` holds the frame every standard shares in `SKILL.md`,
  and one rule file per subject beside it: `comments.md`, `prose.md`,
  `names.md`, `code.md` and `tests.md`.
- `scripts/repo_state.py` runs at the start of every stage and prints what
  the stage needs to know about the repository. `scripts/step_check_prs.py`
  runs at the start of the merge stage.
- `skills/standards/scripts/` holds the step check and the part list
  with their tests: `python3 -m unittest` in that folder.
- `doc/adr/` holds katai's decision records.

## What may go into katai

katai is public and has to work for someone who has never heard of its
author. A sentence belongs in katai only if a stranger with a GitHub
repository could use it unchanged.

- No company, no person, no private repository.
- No tracker product other than GitHub, and no tracker id.
- No product for asking the user or showing a review. katai says "ask the
  owner" and "show this for review". How that happens is the user's own
  configuration.

A standard for comments, code or tests belongs in katai when each of its
sentences names a kind of thing and no product, language or repository. A
repository departs from it by a sentence in its own instruction file.

What holds for one user in every repository belongs in that user's own Claude
Code configuration. What holds in one repository belongs in that repository's
instruction file.

## Changing katai

- Claude Code loads katai from the working tree of the clone it was installed
  from. An edit is live in every new session, and in a running one after
  `/reload-plugins`. Work on a branch in a separate worktree, so that the
  installed clone stays on `main`.
- Commit messages are one line: `type(scope): subject`, imperative and
  lowercase, with no body.
- A change reaches `main` through a pull request, and `main` moves by
  fast-forward.
- To try an install without touching a real configuration, run the install
  command with `CLAUDE_CONFIG_DIR` set to a scratch directory.
