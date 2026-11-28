---
name: plan
description: Open the plan stage of a unit -- create the tracker items that do not exist yet, write one plan per issue in the plans folder, write down the values asked once, and show all plans for one review. Invoked by the owner after the seed report; the invocation is the gate.
disable-model-invocation: true
argument-hint: "[unit slug, only when the plans folder holds more than one unit at this stage]"
allowed-tools: Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/repo_state.py")
---

!`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/repo_state.py"`

# /kt:plan -- the plan stage

Load `kt:workflow` through the Skill tool first. This stage opens on this
invocation and only this invocation. It creates tracker items, writes plans
in the plans folder and writes down the values asked once. It changes no
tracked file, creates no branch and makes no commit.

The argument, when the owner gave one, names the unit:

<unit>
$ARGUMENTS
</unit>

Ask the owner the way the owner's instructions say, and end your turn until
the answer comes; where they say nothing, ask in this conversation. The same
holds for the review this stage shows.

## Entry check

The script's output above, the plans folder it names and GitHub are the
state, read as `kt:workflow`, "What the stage printed", says. The
conversation is no source of state, so the stage runs the same in a cleared
session, from any checkout and from a linked worktree.

- A stop line of the script: stop and say what it printed.
- The unit is the one whose seed report or draft plans the script lists.
  With more than one unit at this stage, the argument names it; without an
  argument, ask the owner which.
- The seed report, `<unit>-seed.md` in the plans folder, is read whole. Its
  sections are the inputs here, and its Code involved section stands in for
  the seed conversation this session may not have had.
- Draft plans of the unit (`plan:` lines with its `Unit:` and
  `Status: draft`): the plans are written, and the stage resumes at the
  review. Read the owner's answer from the owner's review channel. An answer
  goes to step 7. A review that waits unanswered ends your turn. With no
  review sent, go to step 6.
- A plan with `Status: approved` for an issue of the unit is through this
  stage: say so and leave it out.
- No seed report and no draft plan of the unit: stop and say so.
- `owner: unknown` is read as shared.

"The instruction files" below are those Claude Code loaded and the local
note as the script printed it. In a linked worktree the local note reaches
the stage only through that print.

## Step by step

1. Create the tracker item of every issue that has none, one at a time, in
   landing order.

   If a skill in this session covers this repository's tracker, use it for
   this step. The stage keeps the order of the steps and the gates; the
   skill supplies how the step is done.

   The skill gets the issue's title word for word from the seed report, the
   issue's paragraph, and the item of the issue it stacks on. Where no skill
   covers the tracker, the script's tracker evidence decides:
   - GitHub issues in use, which is one or more open milestones or one or
     more issues in 90 days: create the issue.

     ```
     gh issue create -t "<title>" -b "<paragraph>" [-m "<milestone title>"]
     ```

     The body is one paragraph in plain words: what the issue delivers and
     why, from the seed report's Brief and Issues sections, plus one line
     `Depends on #<n>` for a stacked issue. `-m` names the milestone the
     seed report says the unit serves.

   - Another tracker's keys on the `item keys:` line: make the item the way
     the instruction files or the seed report's Where say items are made
     here, a value asked once. Where neither says, or where the tracker
     evidence reads `unknown`, ask the owner how the item is made, because
     a GitHub issue there is a stray item.
   - No tracker at all, which is no open milestone, no issue in 90 days and
     no item keys: make no item. The plan is the item.

   An issue the seed report marks `existing` keeps its item, and this step
   makes nothing for it. An issue a redirect adds gets its item here too,
   with the title its plan gives. Note each item made. A branch name or a
   pull request title of the seed report that holds the item's key as a
   placeholder gets the key now, as `kt:workflow`, "Names", says.

2. Load `kt:standards` through the Skill tool, and read its
   `narrative.md` and `placement.md`.
3. Read `${CLAUDE_SKILL_DIR}/plan-shape.md`, and write one plan per
   issue, `<slug>-plan.md` in the folder of the `plans:` line, in that
   shape, with `Status: draft`. Create the folder when it is missing. The
   header lines are those of `kt:workflow`, "Plans", in its order:
   - `Item:` the item step 1 made; `existing` and the item, for an item the
     unit did not make; or `none`, where the plan is the item.
   - `Unit:`, `Branch:`, `Base:` and `PR title:` as the seed report fixed
     them.
   - `Lands on:` the base, then each release line that takes this issue: a
     line that the instruction files, the seed report's answers or a
     covering skill say takes every merge, and a line that takes a merge
     only when named, where the owner named it for this issue.
   - `Reviewer:` the person who is asked to review: the one the instruction
     files name, else the one the skill that covers pull requests names,
     else the seed report's answer, else the login the `approvals:` line
     counts most often. With none of these, or with the answer "nobody",
     the line is absent.

4. Write down each value the seed report asked once, with the owner's
   answer, as one plain sentence, a "no" included, such as "`release-2.x`
   takes no merges." The sentence keeps the same question from being asked
   again.
   - `owner: shared`: append the sentence to the local note,
     `<main checkout>/.claude/AGENTS.md`, with the main checkout from the
     `checkout:` line. Where the script printed `local note: none` or
     `excluded no`, also add the line `.claude/AGENTS.md` to
     `<main checkout>/.git/info/exclude`, so that `git status` stays clean
     in the checkout and its worktrees.
   - `owner: own`: write the sentence into the Knowledge section of the
     unit's first plan, as a row that lands in the root `AGENTS.md` with a
     `docs` commit of the build.

   In the owner's own repository with no documentation structure, which is
   no root `AGENTS.md` or one whose headings on the `root AGENTS.md:` line
   hold no "Documentation strategy", the unit's first plan proposes the base
   structure: a root `AGENTS.md` with its "Documentation strategy", as the
   first `docs` commit of its Commits and a Rationale row marked
   `proposal`. The owner approves it with the plan, and the sentences of
   this step land in that file.

5. Check the plans. A why you cannot verify, or a function you cannot place
   under the comment rules, is a question to the owner, asked now; the
   answer goes into the plan. What the owner leaves unanswered is an open
   question of the plan-stage message.

   Read each plan as the executor would: for each commit, can each comment
   be composed from its specification alone, with every claim traceable to
   its evidence, and can each of its choices be defended from the Rationale
   alone? Each "no" is a gap in the Design, Rationale or Knowledge section,
   filled now. Then read the plans side by side: a decision two plans rest
   on is a row in both, worded the same; a stacked plan's `Base:` names the
   other plan's branch, and its commits assume only what the other plan's
   commits deliver.

   Run the step check on each plan, with the base directory that the loaded
   `kt:standards` shows:

   ```
   python3 <standards base directory>/scripts/check_steps.py --markdown <plans folder>/<slug>-plan.md
   ```

   Fix every finding in the sketches, and run the check again until its
   last line reports 0 findings. Keep that last line of each plan for step 6. Then read every sketch whose style line says `bare`. Its `because:`
   line says why none of the function's lines makes the reader stop. When a
   sketch lacks that reason, write it if it holds for every line of the
   function. Otherwise sketch the notes or the walkthrough the function
   needs and change its style line.

6. Show all of the unit's draft plans for review in one message, in landing
   order, so that the owner sees a plan before the plan that stacks on it.
   Then end your turn.

   The body, per plan in landing order: one line saying what the issue
   delivers, one line with the last line of the plan's step check from step
   5, then three labeled lists. "Settled by you:" and "Proposed here:" are
   built from the plan's Rationale rows, every row in exactly one of them.
   - "Settled by you:" one line per owner row, the decision and the date,
     nothing else.
   - "Proposed here:" one line per proposal row, the decision, the
     alternative that lost and why, so the owner rules on it here and not
     at the code. A proposal row that adds a type, a trait or a memory
     layout also gets, under its line, a fenced block that shows a caller
     building one and reading a value from it in the language of the code,
     or a drawing of its bytes for a layout.
   - "Where:" one line each for `Item:`, `Lands on:`, `Reviewer:` and the
     merge style of the `merge:` line, each with its source: a script line,
     an instruction file's `path:line`, or the covering skill. A wrong value
     meets the owner here, before any code. Below them, each sentence step 4
     wrote, with where it went.

   A label with no rows is left out. One decision per line, the decision
   before its reason. The approval settles the proposals as it settles the
   open questions.

7. The owner's answer is one of two.
   - An approval. An approval may carry remarks. Apply them, and the
     approval stands for the result. Fold each remark into the plan it
     concerns. A remark about comments rewrites every sketch it concerns,
     as `plan-shape.md`, Design, says, and the step check of step 5 runs
     again on the plans it changed. A remark that corrects a value which
     holds beyond this unit, such as the reviewer or a release line, also
     becomes a sentence as step 4 writes one. The plans count as approved
     without a second review. Change each plan's `Status:` line from
     `draft` to `approved`, so that a cleared session reads them as
     approved, and delete the seed report. Then post the plan-stage message
     and wait. The build stage opens when the owner invokes `/kt:build`.
   - A reply that does not approve is a redirect, also when it only asks
     something back. Answer what it asks, and fold every point of it into
     the plans it concerns. An issue it adds gets its item by step 1 and its
     plan by step 3. Run the
     step check of step 5 again on the plans it changed, and show all of
     the unit's plans for review again from step 6. Never start code on a
     plan the owner redirected.

The plan-stage message, posted on approval, goes to the conversation and is
exactly: one line per issue in landing order with its item (or "no item"),
its branch and its plan's path; one line naming who took the tracker step,
such as "tracker: <skill> <step>", "tracker: gh issue create" or "tracker:
none"; the owner's remarks quoted, if any, with how the plans now honor
them; the sentences step 4 wrote, with where; the open questions the plans
recorded, each with the recommendation the approval has now settled; one
line saying the build waits for `/kt:build`.

Correct: the seed report names two issues, `cache-expiry` and
`cache-metrics`, which stacks on it. The repository's history shows GitHub
issues in use and no skill covers its tracker, so you create issue #41 with
the seed report's title, then issue #42 with `Depends on #41`. You load the
comment guide, write both plans, check them, show both in one review and
end your turn. The owner approves with one remark about a sketch; you
rewrite that sketch, run the step check on that plan, set both statuses to
approved, delete the seed report, post the message and wait.

Incorrect: the owner approves the plans and you create the first branch
because the plans are approved. Or: you show each plan in its own review, so
the owner approves the metrics plan before seeing the cache plan it stacks
on. Or: the approval carries a remark, and you show the plans again and wait
for a second approval. Or: the owner's reply asks why a column is needed,
and you set the plans to approved because the reply sounds friendly. Or: you
shorten the item's title from the one the seed report fixed. Or: the history
shows another tracker's keys and no skill takes the step, and you create a
GitHub issue anyway. Or: the body says what each plan delivers and nothing
else, so the owner meets the planner's choices for the first time beside
the code.
