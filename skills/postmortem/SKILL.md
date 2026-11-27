---
name: postmortem
description: After the last pull request of a unit has merged, reads the owner's remarks on the unit's reviews and returns proposals, each with its home, for the rules that would have prevented the remarks that recur. Loaded by the merge stage with the unit's slug; never invoked by the owner.
user-invocable: false
context: fork
background: false
argument-hint: "<unit>"
allowed-tools: Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/repo_state.py")
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/repo_state.py"`

# The postmortem of a unit

The unit is `$0`. The lines above are what `repo_state.py` printed for this
repository; read them as `katai:workflow`, "What the stage printed", says.
The `owner:` line says whether the repository is the owner's own or shared
with other people, and the `checkout:` line names its main checkout.

You read what the owner remarked while this unit was planned, built and
reviewed. You return proposals for the rules that would have prevented the
remarks that recur. You change no file, and you send no message. Your answer
is the text of one message, and the merge session asks the owner with it.

Four words have a fixed meaning here:

- A mark is something the owner wrote about the unit's work: an annotation
  on a plan, on a review's diff or on a message, the words of a reply, and a
  remark that an approval carries. An answer to a question is not a mark,
  and neither is an approval without remarks.
- A review is one message of the agent that the owner marked: the plan
  review, or the review of one pull request head.
- A class is a kind of defect that recurs.
- A proposal is one change to a rule file, or one added check, that would
  have prevented a class.

## What you read

1. `katai:workflow`, which you load through the Skill tool, and in it the
   section "Changing a rule". It holds the requirements that every proposal
   meets.
2. The marks. Collect the owner's remarks on this unit's reviews from where
   the owner's review channel keeps them. Where it keeps none, say that
   there is nothing to learn from.
3. Each review of the unit. A pull request's review names the pull request
   and the head, and after a reply it names the rule sentence the build had
   followed at the marked places.
4. The commits that answered each reply, with
   `git log --oneline <head the reply marked>..<head of the next review>`.
5. The rule files of the three layers that "Changing a rule" lists, and the
   decision records:
   - this repository's instruction files: its tracked `AGENTS.md` and
     `CLAUDE.md` files, its record folder, and where the repository is
     shared, the local note, whose text ends the lines above
   - katai's files: the skills under `${CLAUDE_SKILL_DIR}/..`, and katai's
     records in `doc/adr/` of the katai clone, `${CLAUDE_SKILL_DIR}/../..`
   - the owner's own configuration: `~/.claude/CLAUDE.md`, and the rules and
     skills under `~/.claude`

## Sort the marks

Give every mark one of three sorts:

- A decision: the owner chooses what the product does. The plan or a
  decision record holds it, and you leave it alone.
- A place: one defect at one spot, fixed in the build, with no sign that it
  recurs.
- A class: marks of the same kind appear in two reviews or more, or the
  owner's words say that it recurs, such as "again", "always" or "you
  keep". The reviews of earlier units count. Find them through the owner's
  review channel in every project, with two or three wordings of the same
  complaint.

Many marks in one review count as one review. They show how large the
defect is, and they do not show that it recurs.

Then say for each class which of four things failed. Quote the rule sentence
that covers the class, or say that none does.

| What failed                              | How you can tell                                                           | The proposal                                |
| ---------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------- |
| No rule covers it                        | no sentence in a rule file speaks to it                                    | a sentence where none was                   |
| A rule covers it, but it is unclear      | the build quoted the sentence and read it another way than the owner       | the same sentence, reworded                 |
| A rule covers it, and it was not applied | the sentence is clear, and the build skipped it                            | a check that cannot be skipped, and no text |
| The rule asks for the wrong thing        | the build applied the sentence as written, and the owner marked the result | the sentence, changed                       |

A class that open rule work already covers gets one line and no proposal.
Open rule work is an open pull request on a `rules-` branch, in this
repository or in katai, or a rule change that waits for the owner's answer.

## Write the proposals

Hold each proposal to every requirement of "Changing a rule", in the order
that section gives them, and write down what you found for each. A
requirement that you did not write down counts as not met. A proposal that
fails a requirement is dropped, and your answer names it under "Dropped". A
decision record that the requirements ask for exists for katai and for a
repository with a record folder; a lesson for a repository without one, or
for the owner's own configuration, has none, and the proposal says so.

Write at most four proposals, the ones with the most reviews behind them, so
that a unit's postmortem costs the owner one message of at most four
questions and one small review. Name the others in one line each under
"Waiting".

Name a home for each proposal. A lesson has one of three homes. A lesson
that holds unchanged for any repository, such as code standards, planning
style or the workflow, is a change to katai. A lesson about this
repository's code, build, layout or people is a sentence in this
repository's instruction file. A lesson about how the owner works across
repositories goes to the owner's own configuration. A lesson takes the home
of the sentence that covers it; with none, the proposal names its home and
the owner's answer may move it. A proposal whose home is katai words its
sentence in general words and names nothing of this repository, because
katai is public; the marks behind it stay in the question's context.

## Your answer

When the unit has no class, answer with one line and nothing else:

```
no class: <n> marks in <m> reviews (<k> decisions, <p> places)
```

When the owner's review channel keeps no remarks on the unit, the line is
`no class: no remarks kept on this unit, so there is nothing to learn from`.

Otherwise answer with the text of the message, in this form, one question
per proposal:

```
Marks in this unit: <n> in <m> reviews: <count> <kind>, <count> <kind>, ...

Covered by open rule work: <class>, by <the pull request or the waiting change>.

Question: <What should change, as a question?>

<Two to four sentences. The marks, each with its date and its review. The
rule sentence that covers the class, quoted, or that none does. Which of the
four things failed. The earlier marks in the opposite direction that you
found, quoted, and why the change does not provoke them.>

Home: <katai | this repository's instruction file | the owner's own configuration>, because <reason>.

- <label>: <the sentence as it would read, or the check, with its file>
- <label>: <a second way to do it>
- No change: <what stays as it is>

Recommended: <one label, word for word>, because <the reason, in one clause>

Not a class: "<the owner's words>" (<review>), once.
Dropped: <proposal>, because <the requirement it failed>.
Waiting: <class>, <n> reviews.
```

A line with nothing under it is left out. The choices stand in their natural
order, and "No change" is always the last one. The recommendation stands
after the choices, never in a label. Add nothing before the first line or
after the last.

You are done when every mark has a sort, every class has its line or its
proposal, and each proposal has its home and has passed every requirement in
writing.

## Examples

Correct: the owner marks a missing step number in two pull request reviews
and one plan review. The rule says that step numbers "match the overview",
and the build read that as allowing a step without a comment. The rule is
unclear. The proposal rewords the one sentence, and its second choice is a
script that checks the numbers. The search for the opposite complaint finds
"the numbering is getting heavy", and the proposal says that the reworded
sentence adds no numbers to a function that has none. Its home is katai,
because the sentence holds for any repository.

Incorrect: the owner writes "too much prose" at three doc comments in one
review. The proposal caps every comment at two lines and adds "most
functions need none". It fails four requirements. One review is a place.
The marks were about doc comments, and the cap reaches every comment. The
sentence sets a quantity. The search would have found a dozen marks that
ask for more comments at the lines. Or: a lesson about this repository's
test command is proposed as a change to katai, so every repository would
carry it.
