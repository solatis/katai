# Lessons and rule changes

`SKILL.md` beside this file is the katai workflow, and the two sections
below belong to it. A stage reads them whole when the owner asks for a rule
to change, before it changes a rule file on a remark or a lesson, and
before it reads or writes the lessons folder.

## Lessons

- The lessons folder of a repository is
  `~/.local/state/katai/github.com/<owner>/<repo>/lessons/`, next to the
  plans folder. Like the plans folder, it
  lies outside every checkout, and nothing in it is committed or pushed.
  The first stage that writes a file there creates the folder.
- It holds one record per unit, `<unit>.md`. Until the record is written
  it may hold `<unit>-asked.md`, the katai rule changes the owner asked for
  during the unit, as "Changing a rule" says, and `<unit>-candidates.md`, the
  postmortem's candidate lessons and the owner's pick while the record is
  made.
- After the unit's last pull request has merged, the postmortem sorts the
  owner's marks on the unit's reviews into candidate lessons, a class or a
  place each, with a one-sentence assessment. The merge stage asks the
  owner which to capture, as a checklist. The postmortem then drafts the
  record: each picked lesson with its evidence and a before and after taken
  from the work, and for a class also the rule that covers it, what failed
  and its home; the others as one line each. The owner reviews the draft,
  and the approved draft is the record. It proposes no rule text.
- The owner curates, because the owner can tell what matters for the units
  to come, and a record that carries every mark at the same weight buries
  the lessons that do.
- No stage turns a record into a rule change, and keeping a lesson asks
  for none. The owner reads the records of several units together, of every
  repository, and changes a rule when the same picked class shows across
  them, as "Changing a rule" says. One unit's
  marks are too few to weigh a sentence against its opposite, and a rule
  rewritten after each unit swings between them.
- A record stays until the owner deletes it. It may quote the owner's words
  and the repository's names, because it stays on this machine.

## Changing a rule

A rule file is any file a stage reads as a rule: a file of katai, an
instruction file of the repository (its `AGENTS.md` files or the local
note), a rule or skill file of the owner's own configuration, or a decision
record that states a rule the code follows. A change to a rule file meets
the requirements below, whoever asks for it: the postmortem, the owner in a
review, or the owner in the chat. The owner's request settles that the rule
changes. The requirements still hold, because they show the owner what the
change costs before the owner approves it.

1. Evidence. The change quotes each remark behind it, with its date and the
   kind of place it was about: a doc comment, the top of a body, a line, a
   test, a plan sketch or a message. The change touches rules for that kind
   of place and for no other. The quotes go to the owner with the proposal
   and stay out of any commit to katai.
2. A class. The remarks come from two reviews or more, or the owner's words
   say that the defect recurs, such as "again", "always" or "you keep". One
   review without such words is a place. A place gets its fix and no rule.
3. What failed. It is one of four things. No rule covers the class. A rule
   covers it and is unclear. A rule covers it and was not applied. The rule
   asks for the wrong thing. A rule that was not applied gets a check that
   cannot be skipped: a script, a line that the harness runs, or a question
   of the cold reader. It gets no further rule text.
4. The sentence. The change quotes the sentence before and after, with its
   file and section. It changes one or two sentences.
5. The replay. For each remark, the change says what the new sentence would
   have produced at that place. Then it searches the owner's earlier
   remarks for the opposite complaint, in every project, through the
   owner's review channel, with two or three wordings, and quotes up to
   three of them. It says why the new sentence does not provoke them, or it
   states the trade.
6. Kind before quantity. A sentence that sets or removes a number, a share
   or a cap, or that says "most", "many" or "few", gives way to a sentence
   about the kind of thing and where it goes. A quantity stays only with its
   reason beside it.
7. The decision records. A rule of weight has a decision record, and its
   "Rejected alternatives" say what lost and why. A change that brings back
   a rejected alternative names it and answers that reason. A change to
   such a rule rewrites its record in the same commit. katai's rules have
   their records in katai's `doc/adr/`. A repository without records, and
   the owner's own configuration, have none, and the proposal says so.
8. A pause. A sentence that a rule change changed changes again only after
   one unit has been built under it. The owner's own words lift the pause.

No stage asks the owner for a rule change. The postmortem drafts the
unit's lessons and the owner picks and reviews them, as "Lessons" says, and a rule
changes when the owner reads the records together and asks for it. During a review the build fixes the
places the owner remarked on and asks for no rule change. When the owner
writes that a rule changes now, it changes in that build, in a commit of its
own, except a rule of katai, which changes only from a session in katai's
own clone. A lesson about how the owner wants the work done goes into a rule file
through this section. A memory note may point at the rule, and it holds no
lesson of its own.

A lesson has one of three homes. A lesson that holds unchanged for any
repository, such as code standards, planning style or the workflow, is a
change to katai. A lesson about this repository's code, build, layout or
people is a sentence in this repository's instruction file. A lesson about
how the owner works across repositories goes to the owner's own
configuration. A lesson takes the home of the sentence that covers it; with
none, the proposal names its home and the owner's answer may move it.

How each lands, once the owner asks for it:

- katai. A stage in another repository never edits katai. Where the owner
  asks there for a katai rule to change, add the owner's words, dated, to
  `<unit>-asked.md` in the lessons folder, and say so in the stage's
  message. The postmortem carries them into the unit's record. The change itself is made in a session in katai's
  clone, as the clone's `AGENTS.md` says, and is stated in general words
  that quote nothing from the repositories the records came from: no file
  name, no code and no other person's remark, because katai is public and
  those repositories may be private.
- The owner's own repository. A commit to its tracked instruction files and
  its decision records, on the branch of the build where the owner asked
  during a build, else on a branch `rules-<name>` with a pull request with
  an empty body and its own review, landed by the repository's merge style.
- A shared repository. Write the accepted sentence into the local note and
  show it in the closing message, with no commit and no record.
- The owner's own configuration. Edit the accepted sentence into its file
  and show the diff in the closing message.

The owner's request is a yes to the change's text, not to a commit, so a
lesson that lands as a commit gets its own review.

Correct: the owner remarks on a missing step number in two reviews. After
the merge, the postmortem drafts the class, the sentence that the build had
read another way, the owner's earlier "don't go overboard with the
numbering", and the unnumbered and numbered steps, after the owner picked
it. Nobody asks about the rule. Some units later the owner reads the records,
finds the same class in two other repositories, and rewords the one
sentence in a session in katai's clone, with its decision record.

Incorrect: the owner writes "too much prose" at three doc comments in one
review, and the session caps every comment at two lines in the next commit.
One review is a place, the cap reaches comments the remarks were not about,
and the sentence sets a quantity. Or: the postmortem's record names a class
whose home is katai, and the merge session opens a rules pull request
against katai's clone from the repository it merged in.
