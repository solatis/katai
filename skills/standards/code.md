# The rules for code

These rules give the shape of code in any language, in every repository.
`SKILL.md` beside this file says how a standard is applied and how a
repository departs from it. `names.md` holds the rules for names.

A rule that a linter of the language can check, such as formatting, line
length, import order, the case of names or a banned function, lives in the
repository's lint configuration, and the instruction files name the command
that runs it. A rule of that kind that the repository wants and its lint
does not carry is proposed as lint configuration, in a Rationale row of the
plan, and not written as a sentence. Where the language cannot follow a
rule here, such as a definition order that its compiler fixes, the language
wins.

## Functions and files

1. A new file reads from top to bottom. A definition comes before its first
   use, and the entry point comes last. An existing file keeps the order it
   has.
2. A function computes its result from its arguments. Input, output and
   mutable state sit at the edges of the program, in functions that decide
   nothing else. A function that both decides and does input or output is
   split where the two meet.
3. A function gets what it uses, such as a store, a clock or a cancellation
   context, as a parameter, and it reaches for no global. Mutable state at
   the level of a module or a package says at its definition why it lives
   there.
4. A function works at one level of the problem. It decides, or it does
   input and output, or it composes other functions. A function that mixes
   levels is split where they meet. Its length does not decide whether it
   is split.
5. Each branch of a function is reached by an input the function can get. A
   branch for a case that cannot happen says why it cannot, and a branch
   that nothing reaches is deleted.
6. An error says what failed and carries the value that caused it. A caller
   tells errors apart by their type or their code and not by their text. An
   error is handled where something can be done about it, and passed up
   unchanged until then. No error is caught and dropped, unless a note at
   that place says why nothing has to be done about it.
7. A call shows what each of its arguments means. A bare `true`, `false`
   or number whose meaning the reader finds only in the signature of the
   function gets a name, as a named argument, a constant or a function of
   its own for each case.

## Modules and design

8. A value is checked once, where it enters the program, and becomes a type
   that holds only valid values. Code past that point trusts the type and
   does not check the rule again. States that exclude one another are one
   type with a case for each, and not several booleans that can also hold
   a combination no state has.
9. A rule, a constant or a conversion has one home. Where a boundary
   between languages or systems forces a second copy, such as a binding or
   a mirrored list of cases, one side is the home, and the other is
   generated from it or pinned to it by a test.
10. Each concern has one convention in a repository. A change that needs a
    second way to do what the tree already does one way, such as a second
    way to report an error or to read configuration, is a Rationale row of
    the plan.
11. An interface, a trait or a generic parameter exists for implementations
    that the tree has. One that only a test implements is a fake, and rule
    14 of `tests.md` holds for it.
12. A dependency between two modules points one way. A module that holds
    the logic of the problem does not depend on a module that does input
    or output for it.
13. A change builds the simple design that meets its outcome. What it
    leaves out on purpose is recorded where the repository records
    decisions, with the evidence that would bring it back.

## Limits

14. Code that nothing in the tree and no public interface reaches is
    deleted, and so is code that is commented out.
15. A change does not rename or remove a public name unless its plan says
    so.
16. Where a measurement shows that a hot path needs a shape these rules
    forbid, such as a buffer reused across calls, the path keeps it, and a
    note at it names the measurement.
17. Vendored and generated code is outside these rules. The input that a
    generator reads is held to them.
18. A change holds the functions it adds or rewrites to these rules. Code
    it only calls stays as it is, and a departure the change finds there
    goes into the report or the plan as a remark and is not repaired.

Correct: a handler parses a request into a type that cannot hold an empty
name, calls a function that decides what to store from that type alone, and
passes the result to the store it was given.

Incorrect: a function reads the clock, decides whether an entry is stale
and deletes it, so that no test reaches the decision without a store and a
real clock. Or: a second module checks the same field again, with a second
copy of the limit. Or: a trait with one implementation is added so that a
test can implement the other.
