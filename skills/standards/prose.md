# The rules for prose

These rules hold for the sentences of every comment and document, in every
repository. `SKILL.md` beside this file says how a standard is applied and how
a repository departs from it.

Comments and documents read like a colleague explaining the code, in plain
sentences. The rules:

1. Every sentence has a subject and a verb and says who does what. Write
   "the importer checks each row against the schema", not "the check is the
   importer's".
2. One idea per sentence. A colon introduces one example or one list of
   nouns, never a chain of clauses, and a semicolon joins nothing.
3. No ellipsis: a sentence does not drop its verb, and a possessive does not
   stand in for a clause ("the handlers' routes_test.py").
4. No rhetoric: no "X, not Y" contrasts except to record a rejected
   alternative, no aphorisms, no mirrored clauses, no "the one", "and
   nothing else", "exactly" or "never" added for emphasis rather than
   meaning.
5. Name the thing: "the standard library parses the body", not "read back
   with the standard library", and "`Validate`", not "the importer's proof".

Read every comment or paragraph back as a colleague would say it aloud. A
sentence that no one would say is rewritten. The rewrite keeps the facts a
reader needs and drops the facts the code already shows. Each sentence below
stands next to what a colleague would write:

| Written                                                                       | A colleague writes                                                                              |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| The handshake is the version check.                                           | Connecting with the client's version is how we check it.                                        |
| A save is never retried, because it is not a read.                            | SaveOrder does not retry, because only reads are safe to run twice.                             |
| The worker runs j as u in u's own sandbox.                                    | Runs the job in the user's own sandbox.                                                         |
| An empty page is read as the end, not fetched again.                          | A query past the last row returns an empty page, which means no rows remain.                    |
| The logging layer wraps every route; the order is the point.                  | Add the logging layer last, so it also wraps `/health`.                                         |
| The status of `o` as a candidate for a refund.                                | Checks whether order `o` can still be refunded.                                                 |
| Runs `fn` with `tx` as the transaction of the connection of the pool.         | Takes a connection from the pool, opens a transaction on it and passes the transaction to `fn`. |
| A cart that holds an item whose stock holds no unit is refused.               | Rejects a cart when one of its items is out of stock.                                           |
| A stale entry is the entry of a key whose age exceeds the limit of its class. | An entry is stale when it is older than its class allows, such as a session after 30 minutes.   |
| Seals the batch before the flush.                                             | Seals the batch, so that no more rows can be added to it, and then writes it to disk.           |

The first five sentences are too clever, and the last five read like a
specification. A sentence of the second kind names a thing by its place among
other things, chains "of" and "whose", or uses a term that nothing has
explained. Its rewrite starts from what the code does and uses the verb a
colleague would say, such as "has" or "contains" where the sentence said
"holds".
