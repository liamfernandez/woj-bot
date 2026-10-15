---
description: Commit current work as a checkpoint on the active branch. Use when the user invokes /checkpoint (optionally with `push` and/or inline guidance), or asks to "checkpoint", "save progress", or "commit what I've got".
---

# Checkpoint

Snapshot in-progress work as a git commit. Frequent, low-ceremony — not polish.

## Parse arguments

Tokenize the argument string on whitespace. Case-insensitive standalone token `push` → set push flag (and remove from tokens). Remaining text → inline guidance (may be empty).

## Pre-commit checks (stop at first failure)

1. **Branch.** `git branch --show-current`. If `main`/`master`/`trunk`/`develop`/`dev`, REFUSE sharply — committing to a protected branch is sloppy, the user knows better. Be irritated, not soft. Offer to cut a feature branch instead. Do not proceed.
2. **Repo state.** Must be a git repo. If `git status --porcelain` is empty, say "nothing to commit" and stop.
3. **Slop scan.** Inspect untracked + modified files for AI/scratch artifacts. Examples:
   - Markdown that reads as AI handoff/plan/scratch: `IMPLEMENTATION.md`, `PLAN.md`, `HANDOFF.md`, `NOTES.md`, `TODO.md`, `CONTEXT.md`, `SUMMARY.md`, `claude-*.md`, `*-summary.md`, anything under a root `.claude/` or `.ai/` scratch dir
   - Step-by-step narrations of what was done / context dumps
   - One-off scripts: `scratch.*`, `tmp.*`, `test-output.*`, `debug.*`
   - OS/IDE noise not gitignored: `.DS_Store`, swap files
   
   Judgment call. Real docs (existing READMEs, design docs the user wrote, anything already tracked) are NOT slop. Test: "would the user be embarrassed if a teammate saw this in the diff?"
   
   Don't delete slop. Just exclude it from staging. List exclusions in the summary.

## Commit

- Stage everything that isn't slop (`git add` specific paths — never `git add -A` blindly past the slop filter). Respect `.gitignore`.
- If inline guidance asks for splitting/grouping, produce multiple focused commits accordingly.
- Otherwise: single commit.
- Message: concise, what-changed, present-tense imperative. Match repo convention from recent `git log` (e.g. conventional commits like `feat:`/`fix:`/`refactor:` if used). No narration, no AI attribution, no `Co-Authored-By: Claude` trailer unless existing commits already do that.
- Never `--amend`. Never rewrite history. Never `--no-verify`.

## Push

- Default (no push flag): commit only. Remind user it's local.
- `push` flag set: `git push` after committing. If no upstream, `git push -u origin <current-branch>`. On rejection or any failure, report plainly. Never force push. Never recover destructively without being asked.

## Summary (after success)

Compact. Include:
- Each commit's short SHA + subject
- Slop excluded (paths), if any
- Push status: `pushed to <remote>/<branch>` OR `not pushed — run /checkpoint push to push`

## Constraints

- User-scoped skill.
- Don't run tests, linters, or builds. Checkpointing ≠ validating.
