---
name: postmortem
description: After the last pull request of a unit has merged, reads the owner's remarks on the unit's reviews. With `candidates`, returns the candidate lessons for the owner to pick from; with `draft`, returns the draft of the lessons record for the lessons the owner picked, each with its evidence and a before and after taken from the work. Proposes and changes no rule. Loaded twice by the merge stage with the unit's slug; never invoked by the owner.
user-invocable: false
context: fork
background: false
argument-hint: "<unit> <candidates | draft>"
allowed-tools: Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/repo_state.py")
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/repo_state.py"`

# The postmortem of a unit

The unit is `$0`, and the pass is `$1`. The lines above are what `repo_state.py` printed for this
repository; read them as `katai:workflow`, "What the stage printed", says.
The `owner:` line says whether the repository is the owner's own or shared
with other people, and the `checkout:` line names its main checkout.

You read what the owner remarked while this unit was planned, built and
reviewed. The merge stage loads you twice, as `katai:workflow`, "Lessons",
says:

1. `candidates`: you sort every mark and return the candidate lessons, one
   short entry each. The merge session asks the owner which to capture, and
   writes the owner's answer below your candidates in
   `<unit>-candidates.md` in the lessons folder.
2. `draft`: you read that file and return the draft of the record, with the
   lessons the owner picked worked out in full, evidence and before and
   after included. The merge session shows the draft to the owner for
   review, and writes the record once the owner approves it.

You change no file, you send no message, and you propose no rule text.

The owner picks, because the owner can tell a lesson that matters for the
units to come from one that does not, and a record that keeps both buries
the first. So each candidate states its assessment plainly enough to be
judged on its own, and leaves the weighing to the owner.

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
- A lesson is one class, or one place: what the owner picks to capture or
  leaves out.
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

## Before and after

In the `draft` pass, each picked lesson carries a before and an after: what the work said at the marked
spot when the owner marked it, and what it said once the remark was
answered. They are the contrast that a later reader weighs a rule against,
and they come from the work, never from you.

- Code and tests: the before is the marked lines at the head the review
  named, from `git show <head>:<file>`, and the after is the same lines at
  the head that answered the reply, found with
  `git diff <head the reply marked>..<head of the next review> -- <file>`.
- A plan or a message: the before is the text the owner's mark quotes or was
  made on, as the owner's review channel keeps it, and the after is the
  same passage in the next version the channel keeps.
- Quote the smallest excerpt that shows the difference, as it is. Where
  the remark was answered by removing the text, the after says
  `(removed)`. Where the channel or git no longer keeps one side, say so in
  its place, and invent neither.
- A class carries one before and after per review it was marked in, from
  the mark that shows the kind most clearly. A place carries its own.

## Your answer

When neither the owner's review channel nor `<unit>-asked.md` keeps a
remark on the unit, answer either pass with one line and nothing else:

```
no record: no remarks kept on this unit
```

Add nothing before the first line of an answer or after its last. A line or
a section with nothing under it is left out. A kind of place is one of those
requirement 1 of "Changing a rule" lists. An assessment states what you
found, in plain words, so that the owner can agree with it or not from that
sentence; it is no rule text, and it does not argue for its own weight.

### The `candidates` pass

Sort the marks, name what failed, search for opposite complaints and name
the homes, as above. Take no before and after yet. Number the lessons `L1`,
`L2` and on, classes first and then places, because the owner picks them
by number and the `draft` pass keeps the numbers:

```
Unit: <unit>
Marks: <n> in <m> reviews: <k> decisions, <p> places, <c> in classes

- L<n>. Class: <the kind of defect, in a few words>
  Assessment: <one sentence: what the work kept doing and why that is a defect>
  Marks: "<the owner's words>" (<review>); ... and <k> earlier units
  What failed: <one of the four>; home: <katai | this repository | the owner's configuration>
  Asked: yes, where an entry of `<unit>-asked.md` is among its marks
- L<n>. Place: <what was wrong, in a few words>
  Assessment: <one sentence>
  Mark: "<the owner's words>" (<review>, <kind of place>)

Decisions: "<the owner's words>" (<review>); ...
```

Shorten a long mark to the words that carry it, with `...` where you cut.

### The `draft` pass

Read `<unit>-candidates.md` in the lessons folder: your candidates, then
`## Owner's answer` with the numbers the owner picked and the owner's words.
Where the file or its answer is missing, answer `no draft: no answer of the
owner in <unit>-candidates.md` and nothing else.

Sort the marks again as above, and keep the numbers of the candidates. For
each picked lesson, take its before and after and work it out in full. Where
the owner's words correct an assessment, the owner's version stands, and
yours follows it as `Earlier assessment:`. Answer in this form:

````
Unit: <unit>
Repository: github.com/<owner>/<repo>, <own | shared>
Date: <YYYY-MM-DD>
Pull requests: #<n> at <head sha>, ...
Marks: <n> in <m> reviews: <k> decisions, <p> places, <c> in classes
Picked: <L1, L3, ...> of <n> lessons

## L<n>. Class: <the kind of defect, in a few words>

- Assessment: <one sentence>
- Owner: "<the owner's words on this lesson>"
- Marks: "<the owner's words>" (<date>, <review>, <kind of place>); ...
- Earlier units: "<the owner's words>" (<date>, <record or project>); ...
- Covering rule: "<the sentence>" (<file>, <section>), or none
- What failed: <one of the four>, because <how you can tell>
- Opposite complaints: "<the owner's words>" (<date>, <project>); ...
- Home: <katai | this repository's instruction file | the owner's own configuration>, because <reason>
- Open rule work: <the pull request>
- Asked: "<the owner's words>" (<date>)

Before (<review>, <file or passage>):

```<language>
<the excerpt>
```

After (<sha or next review>):

```<language>
<the excerpt>
```

## L<n>. Place: <what was wrong, in a few words>

- Assessment: <one sentence>
- Owner: "<the owner's words on this lesson>"
- Mark: "<the owner's words>" (<date>, <review>, <kind of place>)
- Followed: "<rule sentence>", or no rule
- Fixed in: <sha>

Before (...) and After (...), as for a class.

## Not picked

- L<n>. <the heading>: "<the owner's words on the mark>" (<date>)

## Decisions

- "<the owner's words>" (<date>, <review>)
````

The lessons the owner did not pick keep one line each under "Not picked",
with no before and after, so that a later reading can see the same place
recur. The record quotes the owner's words and the repository's names as
they are, because it stays on this machine; whoever later turns it into a
change to katai states the change in general words.

You are done with the `candidates` pass when every mark has a sort and
every lesson its assessment, and with the `draft` pass when every picked
lesson has its before and after, and every picked class its covering rule,
what failed, its search for opposite complaints and its home.

## Examples

Correct: the owner marks a missing step number in two pull request reviews
and one plan review. The rule says that step numbers "match the overview",
and the build read that as allowing a step without a comment. The
candidates list it as L1, a class whose rule is unclear and whose home is
katai, beside L2, a misnamed test in one review. The owner picks L1. The
draft quotes the sentence and the earlier "the numbering is getting heavy"
as an opposite complaint, and under it stand the unnumbered step from each
review and the numbered step the answering commit wrote. L2 is one line
under "Not picked". Neither pass proposes new wording.

Incorrect: the owner writes "too much prose" at three doc comments in one
review, and the candidates list a class with a proposed cap of two lines per
comment. One review is a place, so the marks are one place lesson, and no
pass proposes rule text. Or: the candidates leave out the places because no
class came of them, and the owner never gets to pick the one that matters.
Or: the candidates call a lesson minor, and the owner's weighing starts from
yours. Or: the draft works out a lesson the owner did not pick. Or: the
after is a comment you wrote to show how it should read, and not the one
the answering commit holds.
