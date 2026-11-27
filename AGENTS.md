# katai

katai is a Claude Code plugin that carries a staged workflow into any
repository. `README.md` says what it does for a user. This file is for agents
that change katai itself.

## Layout

- `.claude-plugin/plugin.json` names the plugin. Its skills are typed
  `/katai:<skill>`.
- `.claude-plugin/marketplace.json` lists the plugin with `source: "./"`, so
  that Claude Code can install it from a clone.
- `install.sh` installs the plugin from the clone it sits in, and
  `install.sh --uninstall` removes it.

## What may go into katai

katai is public and has to work for someone who has never heard of its
author. A sentence belongs in katai only if a stranger with a GitHub
repository could use it unchanged.

- No company, no person, no private repository.
- No tracker product other than GitHub, and no tracker id.
- No product for asking the user or showing a review. katai says "ask the
  owner" and "show this for review". How that happens is the user's own
  configuration.

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
- Run `install.sh` against a scratch `CLAUDE_CONFIG_DIR` to try it without
  touching a real configuration.
