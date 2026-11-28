# The rules for comments and prose

These rules hold for the comments and documents of every repository.
`SKILL.md` beside this file says how to apply them, and its references hold
the worked examples.

## Code comments

A comment says what the code cannot say for itself, and it is written for the
reader. The reader is a senior engineer who reads a diff cold. The reader
knows the language, its standard library and the common algorithms by name.
The reader has no type hints, has not read the plan, the decision records or
the rest of the module, and does not know the terms this code defines. A
function can carry four kinds of comment: the doc comment above it, the
walkthrough at the top of its body, one back-reference per step of the
walkthrough, and notes at single lines.

1. The doc comment above a function opens with a verb, after the function's
   name where the language's convention puts the name first. It tells a
   caller in one to three sentences what the function does and what it is
   for, then what it returns and how it fails. It says how the function
   works only where a caller needs that to use it, as with a macro or a
   generic helper.
2. Each function gets one of three levels. A function that forwards, passes
   settings through or maps fields one to one is bare, whatever else is true
   of it. A constant in it still says where it came from. Test the other
   functions against the levels in this order, and the first that applies
   wins.
   - Walkthrough: the reader cannot see the function's plan at any single
     line. A function that runs a parse or an algorithm in several phases, a
     function that joins values from several other functions in a way no
     single line shows, and a function whose steps must run in an order that
     needs a reason all qualify. A helper that one of these functions calls
     qualifies only on its own merits. A chain of independent cases qualifies
     when the place of some case in the chain needs a reason. A standard
     algorithm qualifies unless its name already says which variant it is.
     Length and branch count do not qualify a function.
   - Notes: the reader would stop at one or more lines of the function. Each
     such line gets a note, and the body gets no walkthrough.
   - Bare: any other function. Its body has no comment, except that a
     constant says where it came from.
3. The walkthrough is the first comment in the body. It opens with a
   sentence or a short paragraph on what the function does and how. Numbered
   items follow, one per step, counting up from 1. Each item says in a
   sentence what its step achieves at the level of the problem, and leaves
   its values, names and calls to the code. Two steps that share one loop are
   one step. An item adds a fact only where the code does not show it, such
   as why the step exists or why it comes at its place.
4. Two kinds of walkthrough have no numbered items and no back-references.
   The walkthrough of a standard algorithm names the algorithm and its
   variant and states its invariant. A body that tests a chain of independent
   cases, where the first case that applies returns, has no sequence of
   steps. Its walkthrough names the cases whose place in the chain matters,
   and the note at each of those cases says why.
5. A fact sits where its subject is. A fact about a whole step, about the
   order of the steps or about the approach goes in the walkthrough. A fact
   about one line goes at that line as a note. Each fact is stated once.
6. Each numbered item has one back-reference in the body. A back-reference is
   a one-line comment at the first line of its step, with the item's number
   and a few words from the item, such as `// 2. run the grammar`. Every
   number of the walkthrough appears once as a back-reference, in ascending
   order, and every back-reference has its number in the walkthrough. A
   back-reference states no fact of its own, and a bare number such as
   `// 3.` is not a back-reference. A step may begin inside the block of the
   step before it. Code before step 1, such as an early return, carries no
   number. A note about the first line of a step sits directly below the
   back-reference, as a comment line of its own that is not indented under
   the back-reference's words.
7. Every other comment in a body is a note. A note carries no number and sits
   directly above the line it explains. A line gets a note when the reader
   would stop there to work out what the line does or to ask why it is
   there. Readers often stop at a closure, a pattern that takes apart a value
   another function built, a chain of combinators, arithmetic on indexes, a
   guard, a chain of calls on an optional value, and a match arm whose place
   in the match matters. Such a construct gets a note when the reader would
   stop at it. The writer already knows what each line does and cannot see
   where a reader stops. It writes a note at each such construct whose
   effect neither a name nor the line itself states, and the cold reader of
   `kt:doc-read` finds the lines that the writer missed. The note says
   what the line achieves in the terms of the problem, or why the line is
   there. A note that repeats its line in other words is deleted, and so is a
   note that explains what a language feature does in general.
8. A comment gives one concrete case where it states a rule about values,
   such as which inputs match or how two types combine, and where the effect
   of a line is hard to see without one, as at a grammar rule or a match arm
   whose case is not obvious. A comment gives no case where its line already
   shows one. A byte offset appears only where the code computes a range.
9. Numbers appear only in a walkthrough and its back-references. A list
   inside a note uses bullets.
10. Each kind of comment has a normal size. A walkthrough item is one
    sentence, and it grows by one sentence for each fact the code does not
    show. A note is one to three lines, and a back-reference is one line. A
    walkthrough item grows past its size only for a worked example that its
    steps use. A note that holds several facts is split, and each fact moves
    to the line or the step it concerns. No ratio of comment lines to code
    lines applies.
11. Tests follow these rules like any other code. A test that moves the
    system through several states before it checks the result gets a
    walkthrough of its scenario. A check whose expected value is not obvious
    gets a note that says why the value is right.
12. Constants say where they came from, and impossible branches say why they
    are impossible. A construct that looks wrong says which alternative was
    rejected, but only where a reader of that line would propose the
    alternative. Other rejected alternatives belong in a decision record or
    nowhere.
13. A comment describes the code as it is. When code changes, rewrite every
    comment block the change touches from the new code, as if the code had
    always worked this way. The walkthrough is one block, so a change to any
    step rewrites the whole walkthrough and renumbers the back-references.
    Write the new block before rereading the old one, then carry over only
    the facts the code cannot show. A comment never mentions an earlier
    version, a plan, a review, an issue, a unit of work or the conversation
    that shaped it.
14. Only state what is known. When the owner is in the session, an unknown
    reason, or a function you cannot place under the rules above, is a
    question to the owner, asked before the commit that needs it. Never
    invent a reason.
15. After writing a function's comments, read them back top to bottom as
    separate claims and check each against the code below it. Check each
    walkthrough item against the code from its back-reference to the next
    one. Fix or delete any claim the code does not bear out.
16. A comment cites a decision record by its number, as `ADR-<n>`, and not by
    the path of its file. A comment does not say who decided something or
    when, so it holds no bracket with a name and a date, such as one that
    opens with the word owner. The decision record says how the decision was
    made, and it may carry that trace.

This is the primary path: new code is written this way. "The two checks
that run in a subagent" and "Who writes" in `SKILL.md` say how a change is
checked against these rules and who writes its comments.

The step check, `scripts/check_steps.py`, enforces the numbering of
walkthroughs and back-references. It also reports the two forms that the last
rule forbids: a comment that names the path of the repository's folder of
decision records, and a comment that holds an opening bracket followed by the
word owner and a comma. It reads the whole of each file it is given, prints
one line per finding and ends with a line that counts them. It does not read
block comments. It does not check whether a back-reference sits at the right
line, whether a function that needs a walkthrough has one, or whether a
comment is true. `kt:doc-read`, `kt:doc-audit` and the read-back cover
those.

## Prose

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
