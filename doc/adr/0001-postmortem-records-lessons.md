# 0001. The postmortem records lessons and changes no rule

Date: 2026-11-28

## Context

After the last pull request of a unit merges, the postmortem reads the
owner's remarks on the unit's reviews. It used to turn the recurring ones
into proposals, ask the owner, and land the accepted ones at once: a rules
pull request against katai's clone or the repository, or an edit to the
owner's own configuration.

Two things went wrong with that. A rule rewritten after each unit is weighed
against one unit's remarks, and an agent that rewrites rules one unit at a
time over-corrects: the next unit's opposite complaint swings the sentence
back. And the merge stage runs in the repository the unit was built in, not
in katai, so a katai lesson landed from there edits katai from a session
that has no business changing it.

A record written straight from the postmortem has a third problem: it
carries every mark at one weight. The agent cannot tell a remark that
matters for the units to come from a passing one, and a batch reading of
many such records drowns the first in the second.

## Decision

The postmortem runs in two passes. The first sorts every mark and returns
the candidate lessons, a class or a place each, with a one-sentence
assessment. The merge stage asks the owner which to capture, as one
checklist with no recommendation and nothing picked in advance, and the
owner may correct an assessment in words.

The second pass drafts the record from the owner's pick. Each picked lesson
holds its evidence and a before and after: the marked excerpt at the
reviewed head and the same excerpt after the commit that answered it. A
picked class also holds the rule sentence that covers it, what failed, the
earlier opposite complaints and its home. A lesson not picked is one line.
The draft holds no proposed rule text. The merge stage shows it for review,
and writes the approved draft to
`~/.local/state/katai/github.com/<owner>/<repo>/lessons/<unit>.md`. It asks
nothing about rules.

No stage turns a record into a rule change. The owner reads the records of
several units together and changes a rule where a class shows across them,
under the requirements of "Changing a rule". A katai rule changes only from
a session in katai's clone. Where the owner asks for a katai change from
another repository, the request goes into `<unit>-asked.md` in the lessons
folder and the postmortem carries it into the record.

## Rejected alternatives

- Propose and land at merge time, as before. Rejected for the over-correction
  and the cross-repository edit above.
- Record only katai lessons and keep landing lessons for the repository and
  the owner's configuration at merge time. Rejected: the over-correction does
  not depend on where the sentence lives.
- Record proposed sentences beside the evidence. Rejected: a sentence written
  from one unit anchors the later batch reading on that unit's view.
- A stage that reads the records and proposes a batch. Not built yet; the
  owner reads the folder by hand for now.
- Write the record uncurated and let the batch reading weigh it. Rejected:
  the reader of a batch no longer remembers which remark mattered, and the
  owner who made it does, at the end of the unit.
- Draft every lesson in full and let the owner keep or drop each one.
  Rejected: the owner would review the before and after of lessons that do
  not matter, which is the noise the pick removes, and the work of taking
  them is spent for nothing.
- Drop the lessons the owner does not pick. Rejected: a minor
  place that recurs in later units is the evidence of a class, and one line
  keeps it at little noise.
- Let the postmortem propose a pick. Rejected: a weight shown first is the
  weight the owner starts from.

## Consequences

- A merge no longer ends with questions about rules, and no rules pull
  request comes out of a merge. It ends with a checklist of lessons and a
  review of the draft, and the record waits until the owner approves it.
- Lessons wait in the folder until the owner reads them, so a defect may
  recur for a few units before its rule changes.
- Records may quote private repositories; they stay on the machine, and a
  katai change written from them is stated in general words.
