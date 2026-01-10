---
description: Update all sub-applications to their latest versions from GitHub
---

This workflow follows the strict "Host Only" policy where `Trading-Suite` only pulls changes from external repositories.

1.  Discard any accidental local changes in submodules (Strict Enforcement)
// turbo
2.  `git submodule foreach --recursive git restore .`

3.  Pull the latest updates from remote repositories
// turbo
4.  `git submodule update --remote`

5.  Commit the updated pointers to the main repository
// turbo
6.  `git add .`
// turbo
7.  `git commit -m "chore: Update submodule pointers to latest remote versions" || echo "No changes to commit"`
// turbo
8.  `git push`
