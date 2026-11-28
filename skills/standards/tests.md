# The rules for tests

These rules hold for the tests of every repository. `SKILL.md` beside this
file says how a standard is applied and how a repository departs from it. A
test is code that someone maintains, so `code.md` holds for it, and rule 11
of `comments.md` says how it is commented.

## The kinds

1. What a test touches sets its kind. Where each kind lives and how it is
   run are facts of the repository.
2. A unit test runs one piece of logic in the test process and touches
   nothing outside it. It is for logic that stands alone and is easy to get
   wrong, such as a parser, an encoder or a state machine, and that logic
   gets its exhaustive tests there.
3. An integration test drives a component through the interface its callers
   use, in the test process, with its real dependencies. A dependency that
   is a system of its own, such as a database, is live, and the fixture
   provides it. An integration test starts no process of the program under
   test.
4. An end-to-end test runs the built program as its user does, from
   outside, against a live install. It is the only kind that starts the
   program. It lives apart from the unit and integration tests, so that a
   run of those starts no program.
5. The kinds a repository has are its own decision, and a change tests with
   the kinds the repository has. The first test of a kind, such as a first
   end-to-end harness, is a Rationale row of the plan marked `proposal`.
6. A behavior is tested at the lowest kind that reaches it. A unit test
   reaches logic that stands alone. An integration test reaches what needs
   a real dependency. Only what the process alone shows, such as an exit
   code, the usage text or a signal handler, needs an end-to-end test.
   Where the repository has none, that behavior stays untested, and the
   plan says so.
7. Code that forwards, wires components or maps fields one to one is glue.
   Glue gets no unit test, and the integration test of its path covers it.
8. No case is enumerated at two levels. An integration test checks the
   contract with the real dependency, and not the cases of the logic
   beneath it.

## What a test checks

9. A behavior that holds for a set of inputs gets a property test, which
   draws the inputs and states what holds for each. Drawn inputs come from
   a seed that a failing run prints. A case that matters on its own, such
   as a boundary or a fixed defect, gets an example test named after it.
10. A test knows its expected value by construction. It builds the input
    from a value it holds and compares what comes back with that value, and
    it does not compute the expected value with a second copy of the logic.
11. A test checks what a caller can rely on, such as a result, a state or
    the kind of an error. It does not check the wording of a message.
12. No test checks what a library or the language already guarantees. No
    flag, hook or interface exists only for a test unless a Rationale row
    of the plan names it. Making logic stateless is design and not a change
    for the sake of a test.

## Real systems and isolation

13. A test uses the real dependency. A subsystem is anything across a
    process, network or storage boundary, or another component of the
    repository. A fake, mock or stub of a subsystem is a Rationale row of
    the plan that names the subsystem and why the real one cannot serve,
    and a hook that makes a real system fail on demand counts as one. Time
    and randomness are passed in as values and are no subsystem.
14. Each test creates the data it reads and writes, under names no other
    test uses, and removes it. The systems it runs against belong to the
    fixture.

## The language and the existing tests

15. How the language spells a kind, such as the library that draws inputs
    or the command that runs the tests, is what the repository already
    uses, as its dependency manifest, its lint configuration and its tests
    show. Where the tree shows none, the plan proposes one in a Rationale
    row.
16. A change holds the tests it adds or rewrites to these rules and leaves
    the others as they are. A new case in an existing structure, such as a
    table of cases behind one fixture, continues that structure, and the
    plan names the structure. No change rewrites existing tests only to
    bring them under these rules. That is work of its own.

Correct: a change adds a decoder and a route that stores what it decodes.
The plan sketches a property test that decodes drawn values after encoding
them, with the kind `unit`, and one test that stores a record through the
real router and reads it back from the real database, with the kind
`integration`, which does not repeat the decoder's cases.

Incorrect: a change adds a route, and the plan sketches tests of the kind
`integration` that build the binary and start it from the test framework to
call the route. The router reaches the route in the test process. A test
that starts the program is end-to-end, the repository has no such tests,
and nothing the change adds is shown by the process alone. Or: the plan
sketches a unit test against a fake store for each handler that copies a
request into a store call. The handlers are glue, and no Rationale row
names the fake. Or: a test compares an error's text with a string, so a
reworded message fails a test whose contract did not change.
