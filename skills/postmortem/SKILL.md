---
name: postmortem
description: After the last pull request of a unit has merged, reads the owner's remarks on the unit's reviews and returns the text of the unit's lessons record: every mark sorted, and for each recurring class the rule that covers it, what failed and its home. Proposes and changes no rule. Loaded by the merge stage with the unit's slug; never invoked by the owner.
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
reviewed, and you return the text of one lessons record: every mark, its
sort, and for each class the rule that covers it, what failed and where a
lesson would live. You change no file, you send no message, and you propose
no rule text. The merge session writes your answer into the lessons folder,
as `katai:workflow`, "Lessons", says, and asks the owner nothing.

A rule changes later, when the owner reads the records of several units
together. One unit's marks are few, and a rule rewritten after each unit
swings from one unit's complaint to the next one's opposite. So the record
holds the evidence and the diagnosis, and the sentence is written when the
records are read together.

Four words have a fixed meaning here:

- A mark is something the owner wrote about the unit's work: an annotation
  on a plan, on a review's diff or on a message, the words of a reply, and a
  remark that an approval carries. An answer to a question is not a mark,
  and neither is an approval without remarks.
- A review is one message of the agent that the owner marked: the plan
  review, or the review of one pull request head.
- A class is a kind of defect that recurs.
- A record is the file of one unit in the lessons folder.

## What you read

1. `katai:workflow`, which you load through the Skill tool, and in it the
   sections "Lessons" and "Changing a rule". The second says what a later
   rule change needs from a record.
2. The marks. Collect the owner's remarks on this unit's reviews from where
   the owner's review channel keeps them, and the entries of
   `<unit>-asked.md` in this repository's lessons folder, where it exists.
   An entry there is a mark whose sort is a class, because the owner asked
   for the rule to change. Where neither keeps a remark, say that there is
   nothing to record.
3. Each review of the unit. A pull request's review names the pull request
   and the head, and after a reply it names the rule sentence the build had
   followed at the marked places.
4. The commits that answered each reply, with
   `git log --oneline <head the reply marked>..<head of the next review>`.
5. The records of earlier units, in every repository's folder under
   `~/.local/state/katai/lessons/`.
6. The rule files of the three layers that "Changing a rule" lists, and the
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
  keep". The reviews of earlier units count. Find them in the records of
  earlier units and through the owner's review channel in every project,
  with two or three wordings of the same complaint.

Many marks in one review count as one review. They show how large the
defect is, and they do not show that it recurs.

Then say for each class which of four things failed. Quote the rule sentence
that covers the class, or say that none does.

| What failed                              | How you can tell                                                           |
| ---------------------------------------- | -------------------------------------------------------------------------- |
| No rule covers it                        | no sentence in a rule file speaks to it                                    |
| A rule covers it, but it is unclear      | the build quoted the sentence and read it another way than the owner       |
| A rule covers it, and it was not applied | the sentence is clear, and the build skipped it                            |
| The rule asks for the wrong thing        | the build applied the sentence as written, and the owner marked the result |

Then search the owner's earlier remarks for the opposite complaint, as
requirement 5 of "Changing a rule" says, and quote up to three of them. A
class that open rule work already covers says so. Open rule work is an open
pull request on a `rules-` branch, in this repository or in katai.

Name a home for each class. A lesson has one of three homes. A lesson that
holds unchanged for any repository, such as code standards, planning style
or the workflow, is a change to katai. A lesson about this repository's
code, build, layout or people is a sentence in this repository's
instruction file. A lesson about how the owner works across repositories
goes to the owner's own configuration. A class takes the home of the
sentence that covers it; with none, name the home that fits.

## Your answer

When neither the owner's review channel nor `<unit>-asked.md` keeps a
remark on the unit, answer with one line and nothing else:

```
no record: no remarks kept on this unit
```

Otherwise answer with the text of the record, in this form:

```
Unit: <unit>
Repository: github.com/<owner>/<repo>, <own | shared>
Date: <YYYY-MM-DD>
Pull requests: #<n> at <head sha>, ...
Marks: <n> in <m> reviews: <k> decisions, <p> places, <c> in classes

## Class: <the kind of defect, in a few words>

- Marks: "<the owner's words>" (<date>, <review>, <kind of place>); ...
- Earlier units: "<the owner's words>" (<date>, <record or project>); ...
- Covering rule: "<the sentence>" (<file>, <section>), or none
- What failed: <one of the four>, because <how you can tell>
- Opposite complaints: "<the owner's words>" (<date>, <project>); ...
- Home: <katai | this repository's instruction file | the owner's own configuration>, because <reason>
- Open rule work: <the pull request>

## Places

- "<the owner's words>" (<date>, <review>, <kind of place>): followed "<rule sentence>", or no rule; fixed in <sha>

## Decisions

- "<the owner's words>" (<date>, <review>)
```

A kind of place is one of those requirement 1 of "Changing a rule" lists. A
line or a section with nothing under it is left out. The record quotes the
owner's words and the repository's names as they are, because it stays on
this machine; whoever later turns it into a change to katai states the
change in general words. Add nothing before the first line or after the
last.

You are done when every mark has a sort and every class has its covering
rule, what failed, its search for opposite complaints and its home.

## Examples

Correct: the owner marks a missing step number in two pull request reviews
and one plan review. The rule says that step numbers "match the overview",
and the build read that as allowing a step without a comment. The record
lists one class with the three marks, quotes the sentence, says that it is
unclear, quotes the earlier "the numbering is getting heavy" as an opposite
complaint, and names katai as its home. It proposes no new wording.

Incorrect: the owner writes "too much prose" at three doc comments in one
review, and the record lists a class with a proposed cap of two lines per
comment. One review is a place, so the marks go under Places, and a record
proposes no rule text. Or: the record leaves out the places because no
class came of them, and the next unit's record cannot show that the same
place recurred.
