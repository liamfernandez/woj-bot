---
description: Rebuild situational awareness about the current branch after a context clear or when picking up work cold. Use when the user invokes /familiarize (with or without a focus prompt), or asks to "catch me up", "where were we", or "get up to speed on this branch".
---

# Familiarize

Inspect local state, recent history, and any open PR to produce a compact "here's where we are" summary. Output is read by both Claude (rebuilding context) and the user (sanity check).

## Invocation

| Form | Behavior |
|------|----------|
| `/familiarize` | Run all checks, produce the standard summary. |
| `/familiarize <prompt>` | Same checks, but weight the summary toward the focus area (e.g. `focus on the auth changes`). |

## Investigation

Run independent steps in parallel. All read-only.

### 1. Branch identity
- `git branch --show-current` — current branch
- `git symbolic-ref refs/remotes/origin/HEAD` — default branch (fall back to `main`, then `master`)
- `git rev-list --left-right --count <default>...HEAD` — ahead/behind

### 2. Working tree
- `git status --porcelain` — list of dirty files
- `git diff` and `git diff --cached` — read the actual changes, not just filenames
- For untracked files that look like real code, `Read` them
- **Scratch/handoff docs** — search for and read any of: `PLAN.md`, `IMPLEMENTATION.md`, `HANDOFF.md`, `NOTES.md`, `SUMMARY.md`, `CONTEXT.md`, `TODO.md`, `claude-*.md`, `*-summary.md`, plus anything under root `.claude/` or `.ai/` scratch dirs. These often contain the plan lost on context clear — they're the single most valuable artifact. Read them in full.

Note rough shape: which modules are touched, what kind of work (feature/fix/refactor/WIP), anything mid-flight or broken.

### 3. Recent commits on this branch
- `git config user.email` — to identify the user's commits
- `git log <default>..HEAD --pretty=format:'%h|%an|%ae|%s|%ar'`
- Cap detailed inspection at the **10 most recent**
- If all/most commits are the user's, read messages and skim diffs (`git show --stat <sha>`) to understand trajectory
- If mixed authors, flag which are the user's

### 4. PR check
- `command -v gh` — if missing, skip and note it
- `gh pr view --json number,title,body,state,isDraft,headRefName,baseRefName,url,additions,deletions`
- Exit code 0 → read the body (often contains intent/plan), note state (draft/open/merged/closed)
- Non-zero → no PR; note and move on

## Output

Compact. Omit empty sections. Should fit on one screen.

```
**Branch:** `<name>` — <N ahead, M behind <default>>

**PR:** #<number> <title> — <state> · <link>
> One-paragraph distillation of the PR body's intent.

**Recent commits** (most recent first):
- `<sha>` <subject> — <relative time>
- ...
<One-line note on overall trajectory.>

**Working tree:** <N modified, M untracked, K staged>
- <Module/area>: <what's happening there, mid-flight notes>
- ...

**Plan/handoff docs found:**
- `<path>` — one-line summary

**Current read:**
<1–2 paragraphs synthesizing where the work is, what the goal seems to be, and the natural next step. This is the part the user actually cares about.>
```

If a focus prompt was given, bias `Current read` (and section ordering if helpful) toward that area. Don't fabricate detail in unrelated sections.

## Constraints

- **User-scoped skill.** Read-only.
- No file modifications, no staging, no commits, no builds, no tests.
- No `git fetch` or other network ops. `gh` calls are the only network access allowed.
- Don't speculate beyond evidence. If the diff is ambiguous, say so — don't invent intent.
- Be concise. A wall of text defeats the purpose.
