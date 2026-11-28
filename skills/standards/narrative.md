# Comments inside functions

Goal: the reader that `comments.md` defines can change a function safely after
reading its doc comment, its walkthrough when it has one, and its notes. Each
fact sits at the scope it is about, and every comment describes the code as
it is today.

The rules are `comments.md` and `prose.md`. This file says how
to apply them and shows examples. The examples are illustrations of shape. Do
not copy their wording or their semantics.

## Which level a function gets

Each function gets one of three levels. Rule 2 of `comments.md` says when a
function qualifies for each, which functions are bare whatever else is true
of them, and that the first level that applies wins. The levels, in the
order of the test:

1. Walkthrough. The reader cannot see the function's plan at any single line.
   The function gets a doc comment, a walkthrough at the top of its body, one
   back-reference per numbered step, and a note at each line where the reader
   stops.
2. Notes. The reader would stop at one or more lines of the function. It gets
   a doc comment and a note at each such line.
3. Bare. Any other function. Its body has no comment, except that a constant
   says where it came from. It gets a doc comment only where the language's
   convention for public items wants one.

Length and branch count do not move a function between levels. A function
with five obvious branches is bare, and a function with one dense line gets
one note.

Record the decision for every function in scope as one row of the plan before
changing anything:

| function (file:symbol) | level | lines where the reader stops | evidence for each reason |
| ---------------------- | ----- | ---------------------------- | ------------------------ |

The column "lines where the reader stops" lists each line that gets a note,
with the question the note answers. The column "evidence for each reason"
lists, for each reason you intend to write in a walkthrough or a note, where
you verified it: a `file:line`, a test, a doc passage or a commit. A reason
without evidence is not written. The function goes under "Rationale unknown"
instead.

## Sizes and the step check

Rule 10 of `comments.md` gives the size of each kind of comment. A comment
above its size usually holds a second fact. Split it, and move each fact to
the step or the line it concerns.

The step check is `scripts/check_steps.py` under the base directory of this
skill. Run it over the source files in scope, with the deny patterns that
step 1 of `checks.md` names:

```
python3 <base directory>/scripts/check_steps.py [--deny REGEX]... <path>...
python3 <base directory>/scripts/check_steps.py --markdown <file.md>
```

The second form checks the fenced code blocks of a Markdown file whose fence
names a language. The script prints one line per finding and ends with a line
that counts them. It checks the step numbers, the back-references and the
denied patterns. It does not check whether a back-reference sits at the right
line, whether a function that qualifies has a walkthrough, or whether a
comment is true.

## Examples

### A forwarder

INCORRECT:

```
/// Sends message `m` with the default timeout.
send(m) -> result
{
    // Get the default timeout
    t = default_timeout()

    // Call send with the timeout
    return send(m, t)
}
```

CORRECT:

```
send(m) -> result
{
    return send(m, default_timeout())
}
```

Every comment in the first version repeats the line below it.

### An algorithm, in pseudocode

The function decides whether a price alert fires for a listing. The reader
cannot see from any single line why it loops over prices or when the
fallbacks decide, so it gets a walkthrough.

CORRECT:

```
/// Decides whether alert `a` fires for listing `l`. It never raises on bad
/// data.
/// The fallbacks on `a` decide listings without a price and prices in an
/// unknown currency.
alert_fires(a, l) -> bool
{
    // A listing can quote several prices, one per seller. The alert fires
    // when any price falls below its limit. The fallbacks on `a` decide only
    // when no price can.
    //
    // 1. We collect the prices of the listing. When there is none, the
    //    no-price fallback decides.
    // 2. We convert each price to the currency of the alert and compare it.
    //    Both run in one loop, so the first price below the limit skips the
    //    remaining conversions.
    // 3. When no price converted, the currency fallback decides.

    // 1. collect the prices
    prices = offers_of(l)
    // A listing whose sellers all withdrew quotes no price, which counts as
    // none.
    if is_empty(prices) or all_withdrawn(prices)
    {
        return apply_fallback(a.on_no_price)
    }

    // 2. convert and compare
    any_converted = false
    for p in prices
    {
        // A withdrawn or unconvertible price is skipped, because the others
        // can still decide the alert.
        if is_withdrawn(p) { continue }
        x = convert(p, a.currency)
        if is_failure(x) { continue }
        any_converted = true
        if x < a.limit { return true }
    }

    // 3. apply the currency fallback
    return any_converted ? false : apply_fallback(a.on_unknown_currency)
}
```

The walkthrough says how the function works and why each step is there, and
each back-reference only names its step. The two facts about single lines,
the withdrawn sellers and the skipped price, sit at those lines as notes
without numbers.

INCORRECT:

```
alert_fires(a, l) -> bool
{
    // 1. collect the prices of the listing
    // 2. convert each price to the currency of the alert
    // 3. compare, firing when any price falls below the limit

    // 1. A listing whose sellers all withdrew quotes no price, which
    //    counts as none.
    prices = offers_of(l)
    ...

    // 2. and 3. share one loop, so the first price below the limit skips
    //    the remaining conversions.
    any_converted = false
    for p in prices
    ...
}
```

The walkthrough lists labels, and the reasons sit in numbered paragraphs in
the body, so the reader learns how the function works only at its end. Steps
2 and 3 run in one loop, so they are one step, and the walkthrough gives them
one item.

### How much an item says, in pseudocode

An item is brief where the code of its step shows the rest, and it says more
where the step rests on a fact that no line shows.

CORRECT:

```
/// Places order `o` and returns its receipt. Fails when a line is invalid,
/// the stock is short or the card is refused.
checkout(o) -> receipt
{
    // We check the order, take the stock and the payment, and store it.
    //
    // 1. We check the order's lines.
    // 2. We reserve the stock before we charge the card. A refused card then
    //    only releases the reservation, which the customer never sees. In the
    //    other order, a shortage after the charge would need a refund.
    // 3. We store the order and return its receipt.

    // 1. check the lines
    check_lines(o.lines)?

    // 2. reserve, then charge
    r = reserve(o.lines)?
    charge(o.card, o.total).or_else(e -> { release(r); fail(e) })?

    // 3. store the order
    return store(o, r)
}
```

Items 1 and 3 are brief, because their code shows the rest: the limits of a
line sit in `check_lines`, and `?` passes its error on. Item 2 says more,
because no line shows why the reservation comes first.

INCORRECT, elaborate where the code shows it:

```
    // 1. We refuse an order without lines, with more than 500 lines or with
    //    a quantity outside 1 to 9999, and the caller gets the error.
```

The item copies the limits of `check_lines` and the work of `?`. The reader
finds both at their lines, and the item goes wrong when a limit changes.

INCORRECT, brief where the code does not show it:

```
    // 2. We reserve the stock and charge the card.
```

The item names the step and drops the reason for its order. Nothing then
stops a reader from swapping the two calls, which brings refunds to the
customer.

### A dense line, in pseudocode

The line joins the operands of a chain such as `a - b - c`. `rest` comes from
a parser elsewhere in the module.

INCORRECT, bare:

```
expr = fold(rest, first, (left, (op, right)) -> binary(op, left, right))
```

The reader does not know what each item of `rest` holds, or in which
direction the chain groups.

INCORRECT, a paraphrase:

```
// Fold `rest` into `first` with a closure that takes apart each pair and
// builds a binary node.
expr = fold(rest, first, (left, (op, right)) -> binary(op, left, right))
```

The note names the fold and the closure, which the reader can already see,
and leaves both questions open.

CORRECT:

```
// Groups the chain from the left, so `a - b - c` reads as `(a - b) - c`.
// Each item of `rest` is an operator and the operand after it.
expr = fold(rest, first, (left, (op, right)) -> binary(op, left, right))
```

The note says what the line achieves for the expression and gives the shape
of the value another function built. The example input shows the grouping
that the fold produces.

### A step that begins inside the step before it, in Rust

```rust
pub fn import(path: &Path) -> Result<Catalog, ImportError> {
    // Importing works as follows:
    //
    // 1. We read the rows of the file. `read_rows` does not fail. A row it
    //    cannot split ends the list in a `Broken` row, and the check reports
    //    it only when it gets there, so errors come in the order of the file.
    // 2. We check the rows against the schema. It gives a catalog, no
    //    catalog, or a refusal such as `UnknownColumn` for a column `pirce`.
    // 3. On a catalog, we resolve the names of the parents. The check holds
    //    each parent as a name, because a row may name a parent that comes
    //    later in the file.
    // 4. Otherwise we build the error from the refusal and from the log of
    //    the column tests. A generic "expected" error first gets two targeted
    //    reasons tried, and neither changes which files are valid.

    // 1. read the rows
    let rows = Rows::new(path, read_rows(path));

    // 2. check the rows
    let refusal = match check(&rows, 0) {
        Ok(Some((mut catalog, _))) => {
            // 3. resolve the names
            resolve(&mut catalog);
            return Ok(catalog);
        }
        // Without a catalog, the log is the only source of the error, as for
        // a file that holds a header and no row.
        Ok(None) => None,
        Err(refusal) => Some(refusal),
    };

    // 4. build the error
    let error = explain(&rows, refusal);
    // A refusal or a reason from `read_rows` already says what is wrong.
    if !matches!(error.reason, Reason::Expected { .. }) {
        return Err(error);
    }
    // A `;` between the columns, as in `a;b;c`, then a header row that comes
    // again further down.
    let targeted = wrong_separator(&rows).or_else(|| repeated_header(&rows));
    Err(targeted.unwrap_or_else(|| with_columns(&rows, error)))
}
```

Step 3 begins inside the arm of step 2 that holds a catalog, so its
back-reference sits at the first line of that arm. Step 2 goes on with the
other two arms, and step 4 begins after the match. The three notes carry no
number, because each explains one line: the arm without a catalog, the guard
and the targeted reasons.

### A doc comment that explains the implementation, in Go

INCORRECT:

```
// Get returns the object stored under key. The circuit gates the call. The
// shard of the key holds the object, loading it from the store on a miss,
// and returns it. The store's IsEvicted and Entry.Release decide from the
// load's error whether the shard keeps the entry. This layer adds two
// decisions, both per store. Only errors that are evidence about the store
// (IsUnavailable) feed the circuit. A read can opt in to one retry after a
// timeout, and a missing key is never retried. A retry after an evicted
// entry runs a fresh load, because the shard dropped the old one. A retry
// after any other timeout may reuse the pending load.
func (c *Cache) Get(ctx context.Context, key string, opts ...GetOption) ([]byte, error) {
```

CORRECT:

```go
// Get returns the object stored under key. It returns a *CircuitOpenError
// while the store is unreachable. WithRetry allows one retry after a
// timeout.
func (c *Cache) Get(ctx context.Context, key string, opts ...GetOption) ([]byte, error) {
	...
		// The caller's own cancellation says nothing about the store.
		if callerLeft(err) {
			return nil, err
		}
		c.recordFailure(err)
		// A second load of a missing key finds it missing again.
		if !o.retry || !isTimeout(err) || errors.Is(err, ErrNotFound) {
```

The first version tells callers how the shards and the circuit work, and each
change to `Get` added a clause to it. The second version tells callers what
they need and puts each reason at the line it explains. The facts about the
shards belong to the shard's own comments.

### A change, in Rust

The code before the change:

```rust
/// Returns the discount on order `o`: 10 percent of its total.
fn discount(o: &Order) -> Money {
    // TODO(pricing): no discount on small orders.
    o.total / 10
}
```

The change adds a threshold. INCORRECT, the old comment patched:

```
/// Returns the discount on order `o`: 10 percent of its total, and now only
/// for a total of 100 or more.
fn discount(o: &Order) -> Money {
    // The threshold replaces the earlier discount on every order.
    if o.total < Money(100) {
        Money(0)
    } else {
        o.total / 10
    }
}
```

CORRECT, the comment written from the new code:

```rust
/// Returns the discount on order `o`: 10 percent of a total of 100 or more,
/// and nothing on a smaller total.
fn discount(o: &Order) -> Money {
    if o.total < Money(100) {
        Money(0)
    } else {
        o.total / 10
    }
}
```

The patched version keeps the words about every order, adds "now", and
explains the history in the body. The rewritten version reads as if the
function had always had the threshold.

### How much a comment says

A comment can be short or long, and either can be right. These four cases
show when.

Short, and right. The line shows everything except where the number came
from, and the comment says that.

```python
# The payment API blocks a client after six failed calls.
MAX_RETRIES = 5
```

Long, and right. A caller cannot use this helper without knowing what happens
to a call that arrives too early, so the doc comment says how it works and
gives a case.

```ts
/**
 * Calls `fn` at most once per `wait` milliseconds. A call that arrives
 * during the wait is not dropped. The last one runs when the wait ends, so
 * a search box still sends the final keystroke.
 */
function throttle<A extends unknown[]>(fn: (...args: A) => void, wait: number);
```

Short, and wrong. The comment has no verb, and it uses "quota", "tenant" and
"plan" as if the reader knew how they relate.

INCORRECT:

```go
// The quota of u as a tenant of the plan.
func quota(u User) int {
```

CORRECT:

```go
// quota returns how many projects user u may create. The limit comes from
// the plan of the user's tenant, and a tenant without a plan gets the free
// limit.
func quota(u User) int {
```

Long, and wrong. The comment repeats the query in words and leaves out what
the query is for.

INCORRECT:

```sql
-- Select the id and the email from users where active is true and
-- created_at is more than 30 days ago, ordered by created_at descending,
-- limited to 100 rows.
SELECT id, email FROM users
WHERE active AND created_at < now() - interval '30 days'
ORDER BY created_at DESC LIMIT 100;
```

CORRECT:

```sql
-- Selects the accounts due for the 30-day follow-up mail, newest first.
-- The mail provider accepts 100 mails per call.
SELECT id, email FROM users
WHERE active AND created_at < now() - interval '30 days'
ORDER BY created_at DESC LIMIT 100;
```

A comment grows when the reader lacks a fact, and it shrinks when the code
already shows the fact. The length of the code does not decide either.

## Applying it to existing code

1. Decide the level with the ordered rules above. A bare function loses its
   noise comments, and nothing else changes. Commented-out code is reported
   under "Needs a human" and stays in place.
2. Read the whole function and what its callers expect before writing.
3. Write the function's comments from the code, before you reread the
   existing ones. Then compare with the existing comments and carry over
   only what the code cannot show: a verified reason, a `TODO(name)` or
   `XXX(name)` tag, a name a reader searches for. Existing wording does not
   survive because it is there. A comment that reads as a patch on an
   earlier version is rewritten whole, even when every clause is true. Where
   the stage printed `owner: shared`, this holds for the blocks the owner
   wrote, and "Held to the owner's lines" in `checks.md` says what happens
   to a block of another author.
4. When the why cannot be verified, write the what and ask the owner for
   the reason. An audit lists the function under "Rationale unknown" as a
   question. Leave performance motives and history to the owner's answer.
5. When the walkthrough needs more than about seven steps, the function is a
   split candidate. Comment it as it is and list it under "Needs a human".
   A standard algorithm, and a body that tests a chain of independent cases,
   get a walkthrough without numbers, as rule 4 of `comments.md` says.
6. Read the comments back in three passes, in this order:
   1. Truth. Read each comment as a separate claim and check it against the
      code directly below it. Check each walkthrough item against the code
      from its back-reference to the next one. Check each example input by
      tracing it through the code or running it in a test, and delete an
      example you cannot check. Run the step check and fix each finding.
   2. Cut. Delete or rewrite each of these comments:
      - a note that repeats what the line below it says
      - a note that restates a walkthrough item
      - a walkthrough item that restates the values, names or calls of its
        step
      - a walkthrough sentence about one line, which moves to that line as a
        note
      - a note that explains what a language feature does in general
      - a byte offset where the code computes no range
      - a number outside a walkthrough and its back-references
      - a comment that mentions an earlier version, a plan, a review, an
        issue or the conversation
      - a mark of who decided something or when, which belongs in the
        decision record
      - a citation of a decision record in a form other than the one rule 16
        of `comments.md` names
      - an implementation detail in a doc comment that a caller does not
        need
      - a rejected alternative that a reader of that line would not propose
      - a sentence that reads like one of the "Written" sentences in the
        table of `prose.md`
   3. Gaps. The session that wrote the code does not judge its own gaps,
      because it already knows what each line does. It runs `kt:read`
      as `checks.md` says and closes each stop the reader lists. An audit
      lists each line where the reader would stop, and each function that
      qualifies for a walkthrough and has none, as a question under
      "Rationale unknown".
7. New code elsewhere in this repository follows the same rules from the
   start. "Repairing existing code and documents" in `SKILL.md` is the
   repair path.
