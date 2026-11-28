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

## Decision

The postmortem returns a lessons record and the merge stage writes it to
`~/.local/state/katai/lessons/github.com/<owner>/<repo>/<unit>.md`. A record
holds every mark with its sort, and for each class the rule sentence that
covers it, what failed, the earlier opposite complaints and its home. It
holds no proposed rule text, and the merge stage asks the owner nothing
about it.

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

## Consequences

- A merge no longer ends with questions about rules, and no rules pull
  request comes out of a merge.
- Lessons wait in the folder until the owner reads them, so a defect may
  recur for a few units before its rule changes.
- Records may quote private repositories; they stay on the machine, and a
  katai change written from them is stated in general words.
