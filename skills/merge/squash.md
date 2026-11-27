# Squash

The base takes each pull request as one commit, with the subject
`<PR title> (#<n>)` and an empty body, so the base holds one line per
change. Never force a push of the base or of a release line.

For each pull request, in landing order:

1. Note the head SHA of the `pull request:` line as `<old head>`, then
   squash it, with the plan's `PR title:`:

   ```
   gh pr merge <n> --squash --subject "<PR title> (#<n>)" --body ""
   ```

   `--subject` is passed because GitHub's default subject depends on the
   repository's settings. `--body ""` overrides the default body, which in
   many repositories joins the commit messages. The command takes no
   `--delete-branch`, because that option deletes the branch before its
   stacked children are retargeted, and it checks out the base in the
   current checkout, which a linked worktree must not do.

2. Verify instead of assuming:

   ```
   gh api repos/<owner>/<repo>/pulls/<n> --jq '.merged, .merge_commit_sha'
   git fetch origin <base>
   git log -1 --format=%s <merge sha>
   ```

   The pull request is merged, and the subject is the one step 1 passed. A
   wrong subject or body on the base is shared history: report it, and do
   not rewrite it. The commit that landed is `<merge sha>`, and a release
   line takes it with `git cherry-pick <merge sha>`.

3. Retarget every open pull request whose base is this branch, before the
   branch goes, because GitHub closes a pull request whose base branch
   disappears: `gh pr edit <child> --base <base>`.
4. Rebase each child onto the base. After a squash the child is no
   fast-forward: its branch still holds the parent's commits, which the base
   holds as one other commit.

   ```
   git rebase --onto origin/<base> <old head> <child branch>
   git push --force-with-lease origin <child branch>
   ```

   Run the rebase in the checkout that holds the child's branch
   (`git -C <that worktree>`), or in this one where none does. The owner's
   invocation is the request for this push. A conflict is a stop for the
   child and for every pull request stacked on it. The child's CI runs again
   on its head and must pass, with the skill that covers CI or
   `gh pr checks <n> --watch`, and its merge state and review decision are
   read again before it lands by step 1.

5. Clean up. In the main checkout (`checkout:` says `main`), first switch
   to the base and bring it to origin, so that the checkout ends on a
   current base; it skips this where another worktree holds the base:

   ```
   git switch <base>
   git merge --ff-only origin/<base>
   ```

   In a linked worktree, never check out the base. Then delete the branch
   locally where no worktree holds it, and on origin. `-D` is needed
   because git does not see a squashed branch as merged.

   ```
   git branch -D <branch>
   git push origin --delete <branch>
   ```

   A local branch that a worktree holds stays, and the closing line names
   it. Where GitHub deleted the branch on merge, nothing is left to delete
   on origin.

Correct: from a linked worktree on `cache-expiry`, you squash #20 with its
subject and an empty body, verify the subject on the base, retarget #21,
rebase `cache-metrics` onto the base with `--onto`, push it with lease,
wait for its CI and its merge state, and squash it the same way.

Incorrect: you squash with `--delete-branch` from a linked worktree, and the
command tries to check out the base there. Or: you squash the child without
the `--onto` rebase, and its squash commit carries the parent's changes a
second time. Or: the subject on the base came out wrong, and you amend and
force-push the base.
