# The milestone gap

Read this where `milestones:` shows one open milestone or more. The
repository plans its work in GitHub milestones, and the candidates are what
the active milestone's goals still need.

A milestone holds goals, never a plan. Its description states its goals,
and where the repository keeps one, a list of what is true when it is done.
Issues are cut from what the active milestone's goals still need, at the
time of the cut, one unit at a time. An issue without a milestone is
free-form work and is equally valid.

## What the instruction files decide

Two things come from the repository's instruction files, and where they are
silent, the owner is asked:

- The order of the milestones, which decides the active one. With one open
  milestone, it is the active one, and nothing is asked. With more, the
  active milestone is the first open one in the order the instruction files
  give, such as "the open milestone with the lowest number is the active
  one". Where they give no order, ask the owner how milestones are ordered
  here, with "lowest number first" and "earliest due date first" as the
  choices, and with history's answer as the recommendation: the order in
  which the recent milestones closed. This is a value asked once, so its
  answer goes into the report's Where as `settled by owner, <date>`, and
  the plan stage writes it.
- Whether a met milestone closes without asking. Where the instruction
  files say so, close it. Where they do not, ask the owner before closing
  it, with the evidence that it is met.

A milestone is met when no issue of it is open and the tree meets every one
of its goals. The command that closes it is
`gh api -X PATCH repos/{owner}/{repo}/milestones/<n> -f state=closed`. A
milestone whose issues are all closed but whose goals the tree does not meet
stays open, and its unmet goals become candidates for the next unit.

## Find the gap

Work through these steps in order; each one feeds the next.

1. The milestone. Read the open milestones with
   `gh api 'repos/{owner}/{repo}/milestones?state=open&per_page=100' --jq '.[] | "\(.number) \(.title) due=\(.due_on) open=\(.open_issues) closed=\(.closed_issues)"'`,
   and take the active one as above. When it has no open issue, run steps 2
   and 3 on it first. When the tree meets every goal, it is met: close it
   as above, and record it with its evidence for the report's Where. Then
   take the next open milestone as the active one and start again from this
   step. With no open milestone left, return to `SKILL.md` and go on as it
   says for a repository without open milestones.
2. Its goals. Read the milestone's description whole
   (`gh api repos/{owner}/{repo}/milestones/<n>`). The goals are `owner` by
   provenance where the repository's instruction file names milestone goals
   among the owner's sources, and `agent` otherwise. Any mechanism the description
   names beyond the goal is `agent`, as `kt:seed` classifies it.
3. The tree against the goals. For each goal, check what the tree already
   delivers: the directories, the code, the tests, `git log`. A goal the
   tree meets is met; say so with the evidence.
4. Candidates, in this order:
   1. work in flight: a plan or an open pull request exists for it;
   2. open issues of the milestone
      (`gh issue list --milestone "<title>" --state open --json number,title,body`);
   3. new issues, each a piece of what an unmet goal still needs that no
      open issue covers;
   4. open issues with no milestone, only where they are small and on the
      subject of a candidate above.

   Every candidate carries its source: an issue number, or the goal it
   serves. Work that no goal and no issue calls for is not a candidate; a
   gap you notice goes under Open questions. An open issue the unit picks
   is an existing item.

5. Return to `SKILL.md`, step 3, with the candidates.

A milestone that has no issues yet, such as one just reached, is cut from
its goals alone. Every candidate is then a new issue, from step 4.3.

An open issue of the milestone that the tree shows as landed is stale. It
is reported and not offered, and it keeps the milestone open until the
owner closes it, because no stage closes an issue outside a merge.

Correct: the instruction file says that the active milestone is the open
one with the lowest number and that a met milestone closes without asking.
Milestone 3 has no open issue, and the tree meets each of its goals, with a
path for each. You close it, record it in Where, take milestone 4 as the
active one and cut its candidates from its goals.

Incorrect: the active milestone's goals are all met and none of its issues
is open, and you report that and stop, instead of closing it as the
instruction file allows and cutting the next one. Or: the instruction file
says nothing about closing, and you close the met milestone without asking.
