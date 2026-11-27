# Fast-forward

The base takes each commit of the pull request as it is, with its SHA, so
the base's history stays the branch's history. GitHub has no merge button
that does this: its rebase-and-merge rewrites every commit. A fast-forward
is a push of the base, and GitHub marks the pull request merged when its
head commit becomes reachable from the base. Never force a push of the base
or of a release line.

For each pull request, in landing order:

1. Make it a fast-forward. When
   `git merge-base --is-ancestor origin/<base> <branch>` fails, the base
   moved since the branch was cut, because another pull request landed
   before it. Note the branch's head as `<old head>`, rebase the branch onto
   the base, and compare:

   ```
   git rebase origin/<base> <branch>
   git range-diff origin/<base> <old head> <branch>
   ```

   Run the rebase in the checkout that holds the branch
   (`git -C <that worktree>`), or in this one where none does. The
   range-diff must show every commit unchanged in content. A conflict, or a
   commit whose content changed, is a stop: the reviewed code is not the
   code that would merge. Otherwise push the rebased branch with
   `git push --force-with-lease origin <branch>`; the owner's invocation is
   the request for this push. Wait for its CI on the head, with the skill
   that covers CI or `gh pr checks <n> --watch`, and read the merge state
   and the review decision again, before going on. A stacked pull request
   whose parent landed in this run is already a fast-forward.

2. Note `git rev-parse origin/<base>` as `<old base>`. The commits that
   land are `<old base>..<head sha>`, and a release line takes them with
   `git cherry-pick <old base>..<head sha>`.
3. Land it. In the main checkout (`checkout:` says `main`), check out the
   base, bring it to origin, fast-forward it to the branch and push it, so
   that the checkout ends on a current base:

   ```
   git switch <base>
   git merge --ff-only origin/<base>
   git merge --ff-only <branch>
   git push origin <base>
   ```

   In a linked worktree, push the head to the base and never check out the
   base there, because the main checkout or another worktree may hold it.
   The worktree keeps its branch. The same push serves the main checkout
   when another worktree holds the base.

   ```
   git push origin <head sha>:<base>
   ```

   No merge commit, ever. A rejected push, because origin moved or a rule
   of the repository wants checks this head lacks, is a stop: report it,
   and never force.

4. Verify: `gh pr view <n> --json state -q .state` reads `MERGED`. When it
   does not, report it and leave the pull request, the branch and the item
   as they are.
5. Retarget every open pull request whose base is this branch, before the
   branch goes, because GitHub closes a pull request whose base branch
   disappears: `gh pr edit <child> --base <base>`. The child is then a
   fast-forward of the base.
6. Delete the branch locally where no worktree holds it, and on origin:

   ```
   git branch -d <branch>
   git push origin --delete <branch>
   ```

   A local branch that a worktree holds stays, and the closing line names
   it. Where GitHub deleted the branch on merge, nothing is left to delete
   on origin.

Correct: from a linked worktree on `cache-expiry`, the base has not moved,
so you push the head's SHA to the base, see the pull request merged,
retarget the stacked child, delete the branch on origin, and leave the local
branch to the worktree.

Incorrect: you land the pull request with GitHub's rebase-and-merge, and
the base takes commits whose SHAs no review named. Or: in a linked worktree
you run `git switch main` to merge, and it fails because the main checkout
holds `main`. Or: the base moved, you rebase and push the base at once, and
a rule that wants checks on the pushed commit rejects it, because the
rebased head never ran CI.
