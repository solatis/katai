# 0003. A stage's output is bounded by kind, and messages for the owner stand alone

Date: 2026-11-28

## Context

A stage fixes the form of its messages: the seed report, the plan-stage
message, the build-stage message, the closing lines of the merge, and the
answers of the two reader skills and the postmortem. Nothing bounded the
text a session writes between tool calls. A build lands many commits and
runs several checks, and a session tends to announce each step, repeat what
a tool printed and restate the plan it follows. That text costs tokens, and
the owner has to read past it to find the messages that matter.

The opposite defect matters as much. "Asking and reviews" asks that a
question carries its context, because the owner reads it cold. The owner
also does not read the whole session, so a message that leans on something
said earlier in it fails in the same way as a question without context.

## Decision

`skills/workflow/SKILL.md` has an "Output" section that every stage reads.
It names two kinds of text and treats them differently.

Text between tool calls is nothing, or one line that says what was found or
decided. It does not announce a step, repeat a tool's output, or restate
the printed lines, a plan, the seed report or a skill's text.

A message for the owner is read on its own. It repeats what the owner needs
to follow it, and it leaves out the rest. A message whose form a stage
fixes holds that form and nothing around it.

A file is read once, and again only when it changed.

The section shortens nothing that another rule asks for: a question keeps
its context, a review its lists, a plan its sections and a comment its
reason.

## Rejected alternatives

- A cap on the words or lines of a message. Rejected: a cap is a quantity
  where the defect is a kind, and a cap on a question or a review cuts the
  context the owner needs.
- One instruction to be concise everywhere. Rejected: it does not tell
  narration from a message the owner reads cold, and it brings back the
  question without context.
- A rule in each stage skill. Rejected: the stages already fix the forms of
  their messages, and the text between tool calls is the same in each.
- No rule, on the ground that the fixed forms are enough. Rejected: the
  fixed forms bound the messages and leave the narration unbounded.

## Consequences

- A session shows less of its progress between tool calls. The tool calls
  and the stage's messages carry it.
- A message for the owner may repeat a fact from earlier in the session.
  That repetition is wanted.
- The rule has no check. Whether it holds shows in the owner's remarks on
  later units.
- By "Changing a rule", the sentences of the section stay as they are until
  one unit has been built under them.
