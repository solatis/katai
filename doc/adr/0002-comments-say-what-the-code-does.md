# 0002. Comments say what the code does, in the words a colleague would use

Date: 2026-11-28

## Context

The comment rules asked for a doc comment that is "the contract for callers"
and "holds no implementation detail", and they allowed an example only where
an effect was hard to see. The "Prose" rules asked for a subject, a verb and
one idea per sentence.

Comments written under these rules said the right thing and were hard to
read. Three things made them so:

- A doc comment named its function by its place among other things, without
  a verb, such as "The status of `o` as a candidate for a refund."
- A sentence chained "of", "whose" and "which", or used a verb such as
  "holds" where a person would say "has".
- A comment used a term that the code defines before any comment had said
  what the term means, and it stated a rule about values without one case.

The sentences were not long. A sentence of this kind passes every "Prose"
rule, because those rules are about the form of a sentence and not about its
words.

Two checks existed and did not stop it. The writer read each comment back as
a colleague would say it aloud, but a writer cannot hear its own sentence as
a stranger does. The cold reader reported a sentence that it understood only
in plainer words, but a reader that is a model understands such a sentence at
once and reports nothing.

## Decision

A doc comment above a function opens with a verb and tells a caller what the
function does and what it is for, then what it returns and how it fails. It
says how the function works where a caller needs that to use it, as with a
macro or a generic helper.

A comment gives one concrete case where it states a rule about values, and
none where its line already shows the case.

The table of `prose.md` shows sentences that read like a
specification next to what a colleague would write. `narrative.md` shows four
cases of how much a comment says: short and right, long and right, short and
wrong, long and wrong. The examples come from no real project.

The cold reader reports what it can see on the page: a doc comment whose
first sentence has no verb that says what the function does, a sentence that
it had to untangle, and a term the code defines that a comment uses before
any comment explains it.

## Rejected alternatives

- A cap on the length of a sentence. Rejected: the sentences that read badly
  were of ordinary length, and a cap is a quantity where the defect is a
  kind.
- A controlled language with a fixed dictionary, where each word has one
  meaning. Rejected: it changes the voice of every sentence to fix a few
  kinds of sentence, and a writer needs a tool outside katai to follow it.
- A list of banned words. Rejected: a word such as "holds" is right in some
  sentences, and a list invites a swap of one word while the sentence keeps
  its shape.
- More rules about the form of a sentence. Rejected: the sentences already
  passed the rules of that kind.
- A rule that every term is defined at its first use. Rejected: the reader
  that the rules describe already does not know the terms the code defines.
  The rule was there and was not applied, so it gets a check and no further
  text.
- Leaving the read-back as the only check on wording. Rejected for the
  reason in the context.

## Consequences

- Comments grow a little where a case or a helper's workings are added. The
  earlier complaint was the opposite one, comments that repeat their code.
  The second sentence of rule 8 and the "long, and wrong" case guard against
  it.
- A reader round returns more rows, because it now reports terms in code
  comments.
- By "Changing a rule", the changed sentences stay as they are until one
  unit has been built under them.
