---
name: merge
description: Open the merge stage -- per pull request in landing order, land each one that GitHub would accept by the repository's merge style, carry it to the release lines its plan names, close or report its tracker item, delete the plan, close the milestone it completes, and after the last pull request of a unit run the postmortem, ask the owner which of its lessons to capture, show the draft for review, and write the lessons record, which changes no rule. Invoked by the owner after reviewing the code; the invocation is the owner's yes on the code.
disable-model-invocation: true
argument-hint: "[item, pull request or branch ...]"
allowed-tools: Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/repo_state.py"), Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/step_check_prs.py")
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/repo_state.py"`

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/step_check_prs.py"`

# /kt:merge -- the merge stage

Load `kt:workflow` through the Skill tool first. An argument, when the
owner gave one, is:

<issues>
$ARGUMENTS
</issues>

Ask the owner the way the owner's instructions say, and end your turn until
the answer comes; where they say nothing, ask in this conversation. The same
holds for every review this stage shows.

The pull requests to merge are those of the issues the argument names, by
item, pull request number or branch, else those the build-stage message of
this session names. With neither, stop and ask the owner which.

## Entry check

The state comes from the two scripts' output above, the plans folder and
GitHub, never from the conversation: a build-stage message that says green
is a claim, and GitHub is the evidence. Read the script's lines as
`kt:workflow`, "What the stage printed", says. The second script prints,
for each of the owner's open pull requests, the last line of the step check
over `origin/<base>...origin/<head>`, held to the change's lines where the
repository is shared.

- A stop line of the script: stop and say what it printed.
- `tracked changes:` other than 0 is a stop, because the merge checks out
  and rebases branches. Untracked files do not matter.
- `base vs origin:` that says the fetch failed is a stop. In the main
  checkout, a local base ahead of origin is a stop, because a fast-forward
  of it would publish commits nobody reviewed; the owner decides.
- `owner: unknown` is read as shared. "The instruction files" below are
  those Claude Code loaded and the local note as the script printed it.

For each pull request to merge, all of these hold:

- Its plan is in the plans folder. A pull request with no plan is not this
  stage's to merge.
- Its `pull request:` line shows it open. A plan whose pull request merged
  is handled by "Merged outside the stages" below.
- Its head SHA on GitHub is the local branch's head
  (`git rev-parse <branch>`; the line shows its first 12 characters), so
  the code that lands is the code that was pushed and reviewed.
- With CI (`ci:` other than `none`), every check on that head passed: the
  line reads `checks SUCCESS`. A check still running or failed stops it,
  and so does `checks none`, because nothing ran.
- GitHub would accept the merge, as the pull request's merge state and
  review decision show; they carry the repository's required reviews and
  checks. The review decision is `APPROVED`, or `none` where the repository
  requires no review. The merge state is `CLEAN` or `HAS_HOOKS`, or
  `BEHIND` under a fast-forward, which `fast-forward.md` rebases. A state
  of `UNKNOWN` is read again with
  `gh pr view <n> --json mergeStateStatus,reviewDecision`, and one that
  stays `UNKNOWN` stops it.
- The step check reports 0 findings for it in the second script's output. A
  finding, or a pull request with no line there, stops it.
- Its base is the base branch, or the branch of a pull request that lands
  before it in this run.
- The owner typed the merge. This invocation is that approval.

The plan's `Reviewer:` is no gate: it names who was asked to review, and
GitHub's review decision carries what the repository requires.

A failure stops that pull request and every one stacked on it; say which
and why, and the owner decides. The others proceed. For a pull request
whose parent lands in this run, read the merge state, the review decision
and the checks again once the parent has landed and the pull request has
been retargeted, because its base changed
(`gh pr view <n> --json mergeStateStatus,reviewDecision,statusCheckRollup`).

Unresolved review threads of other people, which the `threads` count of the
`pull request:` line shows, are listed to the owner with their pull request,
and the merge goes on.

## Merged outside the stages

A plan whose pull request merged, by its branch in the
`branch: merged <k> (...)` line as `<branch> #<n>` or, where no `branch:`
line names the branch, by `gh pr list --head <branch> --state merged`,
merged outside the stages. Report it as "merged outside the stages". When
the argument names it, run what is left of it: step 4 for the item, where
it is still open; step 6 for the milestone; step 5 for the plan and its
check files, which leaves the plan and lists the rows where the audit's
rows are not all settled, and the owner decides; then the postmortem.

## The merge style

The merge style is the one the instruction files name, else the one the
`merge:` line counts for more than half of the pull requests. Read
`${CLAUDE_SKILL_DIR}/fast-forward.md` or `${CLAUDE_SKILL_DIR}/squash.md`,
the one for that style, and read nothing about the other style: the style
file decides how the base takes a change. Where the `merge:` line is
`unknown`, no style has more than half, or the style is merge commits, ask
the owner which of the two files to follow.

## Step by step

For each pull request, in landing order (a pull request after the pull
request its base branch belongs to):

1. Land it as the style file says. The style file also says which commits
   landed and how a stacked child follows its parent.

   If a skill in this session covers this repository's merge, use it for
   this step. The stage keeps the order of the steps and the gates; the
   skill supplies how the step is done.

   The skill supplies the mechanics of the style the style file names, and
   only those.

2. Carry it to its release lines: each line of the plan's `Lands on:` after
   the base. The skill that covers this repository's merge, where one does,
   supplies the conflict rules and the check a line needs before its push.
   Without one, for each line:

   ```
   git fetch origin <line>
   git worktree add --detach <root>/worktrees/<n>-<line> origin/<line>
   git -C <worktree> submodule update --init
   git -C <worktree> cherry-pick <landed commits>
   git -C <worktree> push origin HEAD:<line>
   git worktree remove <worktree>
   ```

   `<root>` is the folder of the `plans:` line without its last part,
   `plans`; a `/` in the line's name becomes `-` in the
   folder's name. The `submodule` line runs only where the `submodules:`
   line counts one or more. Before the push, run in the worktree the check
   the instruction files name for a commit. The pick runs in a detached
   temporary worktree, so no checkout and no worktree that holds the line is
   touched. The pick takes no `-x`, so the subject stays the same on every
   line.

   Resolve only trivial conflicts: generated or vendored files, lock files,
   whitespace, adjacent additions. A conflict in hand-written code is
   aborted with `git -C <worktree> cherry-pick --abort` and reported with
   its files. A failing check or a rejected push is reported the same way.
   In each of these cases the line stays as it is, and the owner decides;
   never force a release line. The temporary worktree is removed in every
   case.

3. Make sure the builds of the base and of each release line run.

   If a skill in this session covers this repository's CI, use it for this
   step. The stage keeps the order of the steps and the gates; the skill
   supplies how the step is done.

   The skill gets the base and each release line with the commit pushed to
   it. Without such a skill, the pushes start what the repository's CI runs
   on a push, and this step starts nothing.

4. Close the tracker item.

   If a skill in this session covers this repository's tracker, use it for
   this step. The stage keeps the order of the steps and the gates; the
   skill supplies how the step is done.

   The plan's `Item:` decides. Tell a covering skill the item and whether
   the plan marks it `existing`: an item that was there before the unit may
   hold more work than this unit, so the skill closes it or leaves it by its
   own rule, and you report which. Without a covering skill, a GitHub issue
   is closed with `gh issue close <n> -c "Landed in #<pr>"`, whoever made
   it, because one issue is one pull request, and an item of another tracker
   is reported and left. With `Item: none` there is nothing to close.

5. Delete the plan and the files of the build's comment checks, but only
   when `<slug>-audit.md` exists and each finding of its "Unlanded from the
   plan" section has an `applied` or `declined` line below the report:

   ```
   rm -f <plans folder>/<slug>-plan.md <plans folder>/<slug>-read-1.md \
     <plans folder>/<slug>-read-2.md <plans folder>/<slug>-audit.md \
     <plans folder>/<slug>-audit-code.md <plans folder>/<slug>-audit-tests.md \
     <plans folder>/<slug>-plan-attack.md <plans folder>/<slug>-build-attack.md
   ```

   Every reason the plan carried is then in the code or the documents, or
   declined with its reason. A missing audit file, or a finding without its
   line, is listed to the owner, and the plan stays, because a reason that
   did not land would be lost with it.

6. Close the milestone this pull request completed. Where the item closed
   in step 4 is a GitHub issue, read its milestone with
   `gh issue view <n> --json milestone -q .milestone.number`, and skip this
   step when it has none. When
   `gh api repos/<owner>/<repo>/milestones/<m> -q .open_issues` is 0, read
   the milestone's goals as `${CLAUDE_SKILL_DIR}/../start-next/milestones.md`
   describes them, and check each goal, or each line of its list of what is
   true when it is done where it has one, against the base as it is now.
   When every one is met, the milestone closes with
   `gh api -X PATCH repos/<owner>/<repo>/milestones/<m> -f state=closed`:
   without asking where the instruction files say so, and after asking the
   owner where they do not. When one is unmet, leave the milestone open,
   because the next unit is cut from it.

The stage posts, replies to and resolves nothing on GitHub in the owner's
name beyond the merge itself, with the retargets and branch deletions it
needs, and the close of the pull request's item.

## The postmortem

Read `${CLAUDE_SKILL_DIR}/../workflow/rule-changes.md` whole before the
steps below. "Lessons" and "Changing a rule" are its sections.

A unit is complete when no plan in the plans folder names it on its `Unit:`
line, which holds from any checkout. List the plans folder again after step
5, because the script's list is from the start of the stage. After the last
pull request of this run, do this for each unit that this run completed:

1. Load `kt:postmortem` through the Skill tool with the unit's slug,
   taken from the plans, and the word `candidates` as its arguments, and no
   other word. The skill runs in a fork of its own, which has not seen this
   session and prints the repository's state for itself. It returns the
   candidate lessons, or one line that starts with `no record`.
2. On `no record`, add that line to the closing lines below, and stop here
   for this unit.
3. Write the candidates as they came into `<lessons>/<unit>-candidates.md`,
   where `<lessons>` is the lessons folder that "Lessons" names.
   Create the folder where it does not exist. The file is how a cleared
   session finds where the postmortem stands.
4. Ask the owner which lessons to capture, in one question where the owner
   picks several, one choice per lesson: its number and heading as the
   label, its assessment and marks as the description. Below the choices,
   say that the owner may correct an assessment in words. The question
   carries no recommendation and nothing is picked in advance, because the
   owner's weighing is what it collects; a lesson marked `Asked: yes` says
   so in its description. The decisions are listed in the question's
   context and are not picked.
5. Append the answer to `<unit>-candidates.md` under `## Owner's answer`:
   the date, the numbers picked, and the owner's words as they came. Where
   the owner picked none, write `<lessons>/<unit>.md` with the header lines
   of the candidates, `Picked: none`, and the lessons as one line each under
   "Not picked", and go to step 9.
6. Load `kt:postmortem` again with the unit's slug and the word `draft`.
   It returns the draft of the record.
7. Show the draft for review. A redirect is folded in: apply the owner's
   words to the draft, or where they change which lessons are picked,
   append them to `## Owner's answer` and run step 6 again, then show the
   result for review again.
8. On approval, write the approved draft into `<lessons>/<unit>.md`,
   replacing a record from an earlier run of this unit.
9. Delete `<unit>-candidates.md` and `<unit>-asked.md`, whose entries the
   record now carries.

Change no rule file: not katai's, not this repository's instruction files,
not the owner's own configuration. A picked lesson is no request for a rule
change. A rule changes only when the owner reads the records of several
units together, as "Lessons" says.

## The closing lines

Close with one line per pull request:
`<branch>: #<pr> merged by <style>, <n> commits, <first sha>..<last sha>`,
plus "rebased first" where the style file rebased; then each release line
with the SHA of its pick, or the reason it stopped; then "item <item>
closed", "item <item> <state>, left" or "no item"; then
", milestone <title> closed" or ", milestone <title> open: <unmet line>"
where step 6 read a milestone; then "plan deleted", or the rows that kept
it; then the number of unresolved threads of other people; then who
took each step, such as "merge: <skill>" or "tracker: gh issue close". Add
one line per pull request that stopped, with the reason, and one line per
postmortem: its `no record` line, or the path of the record with its count
of picked and not picked lessons and of decisions.

Correct: `cache-expiry` (#20) and `cache-metrics` (#21, stacked on expiry)
are green, GitHub would accept #20, and the step check shows 0 findings for
both. The style is fast-forward. You land #20 by `fast-forward.md`, see it
merged, retarget #21 to the base, delete `cache-expiry`, close #41 and
delete its plan. You read #21's merge state again, now against the base,
and land it the same way. #21 closed the last open issue of its milestone,
and the base meets every line of its list, so the milestone closes as the
instruction files say.

Incorrect: you delete `cache-expiry` before retargeting #21, and GitHub
closes #21. Or: the build-stage message said green, the script shows a check
still running, and the merge runs on the message. Or: the push is rejected
and you retry with force. Or: the seed report said the unit finishes the
milestone, and you close it on that claim without checking the list against
the base. Or: GitHub's review decision is `APPROVED` by someone other than
the plan's `Reviewer:`, and you stop the merge for the plan's reviewer. Or:
the `merge:` line says squash, and you also read `fast-forward.md` to be
safe and rebase the branch. Or: you check out the release line in this
checkout to pick onto it, and the checkout fails because another worktree
holds the line. Or: a colleague left two unresolved threads, and you
resolve them before the merge. Or: you tell `kt:postmortem` which remarks
you think matter, so the postmortem sorts them the way the session that
built the code sees them. Or: the record names a class whose home is katai,
and you edit katai's skills from this repository, or ask the owner whether
to change the rule now. Or: you ask which lessons to capture with a
recommendation, or you leave out a place you judge small, so the owner
weighs the candidates as you weighed them. Or: you write the record before
the owner approved the draft. Or: the owner leaves L2 unpicked, and the
record drops it entirely, so a third unit with the same place shows no
earlier one.
