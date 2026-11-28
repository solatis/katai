# 0004. One skill holds the frame of every standard, and one agent per stance reads

Date: 2026-11-28

## Context

katai had a standard for comments and prose, in a skill named
`doc-discipline`, with a step check, two cold reads and an audit. It had no
standard for code or tests beyond a short file of naming rules. Repositories
that used katai wrote their own, each in other words, and where such a rule
had no check it drifted.

A second skill beside `doc-discipline` would have repeated what is not about
comments at all: what a standard is, how a repository departs from one, what
a change is held to, and how a finding is closed. The comment rules are one
standard among several, and the skill that held them was the frame with one
subject in it.

Both reader skills ran on one agent whose prompt was four sentences. The way
each reader thinks was written in its skill, so the cold reader and the
auditor shared a prompt although one must know no rule and the other must
cite one.

## Decision

`kt:standards` replaces `kt:doc-discipline`. Its `SKILL.md` holds the frame
once, and one rule file per subject sits beside it: `comments.md`,
`prose.md`, `names.md`, `code.md` and `tests.md`.

A rule file is the default. A sentence in the repository's instruction files
outranks the owner's own configuration, and both outrank a rule file. A
departure is one dated sentence that names the rule it departs from. What a
repository's code already does is never a rule. katai fixes no place for a
departure: the seed finds where the repository keeps its rules for the
subject and proposes that place for each case.

Comments and documents are held to whole files in the owner's own repository
and to the changed lines in a shared one. Code and tests are held to what a
change adds or rewrites, in every repository, because bringing existing code
under a rule changes what it does.

An agent says who reads, and a skill says what is read and how the answer is
formed. `kt:read` runs on `kt:cold-reader`, which knows no rule and reports
where it stops. `kt:audit` runs on `kt:auditor`, which writes a row only for
a line that breaks a rule it can cite, and takes one subject per run.

## Rejected alternatives

- A sibling skill for code and tests beside `doc-discipline`. It would have
  written the frame twice, and the two copies would have drifted.
- The standards in the owner's own configuration and not in katai. A
  standard whose sentences name kinds of things and no product, language or
  repository works unchanged for a stranger, and a repository that disagrees
  departs by a sentence.
- A fixed home for departures, such as one section of the root `AGENTS.md`.
  Repositories keep their rules in different places, and a shared repository
  may not take a sentence there at all.
- One agent for both readers. The cold reader is useful only while it knows
  no rule, and the auditor only while it cites one.
- A repair of existing code and tests to the standard as part of a change.
  It would widen every change in a repository older than the standard.

## Consequences

Every stage that named `kt:doc-discipline`, `kt:doc-read`, `kt:doc-audit` or
`kt:doc-reader` names `kt:standards`, `kt:read`, `kt:audit`, and
`kt:cold-reader` or `kt:auditor`. A repository's instruction file that names
the old skills by name needs the new names.

A third stance, an attacker that looks for the case a plan or a built change
does not survive, is not part of this decision. It waits until a unit has
been built under the standards for code and tests.
