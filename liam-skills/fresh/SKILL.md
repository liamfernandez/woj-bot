---
description: Start a new feature branch off a fresh pull of main, and (if given a Linear/GitHub issue link) produce an investigation and solution plan. Use when asked to "start a new branch", "branch off main", "fresh branch for X", or when the user invokes /fresh with a description of the work or a ticket link.
---

# Fresh Branch Workflow

Starts a new branch off the latest `main`. The arguments describe the work — infer the branch type and a brief slug from them.

## Steps

1. **Check for uncommitted work.** Run `git status`. If there are uncommitted changes or untracked files that look like in-progress work, STOP and ask the user how to proceed (stash, commit elsewhere, discard). Never silently discard work.

2. **Switch to main and pull.** Run in one chain:
   ```
   git fetch origin && git checkout main && git pull --ff-only
   ```
   If the pull isn't fast-forward, stop and surface the conflict — don't force it.

3. **Derive the branch name** from the arguments:
   - Pick a type prefix based on the described work: `feature/`, `fix/`, `hotfix/`, `refactor/`, `chore/`, `docs/`, `test/`, `devops/`. Match the repo's conventions if this project has a different set (check `CLAUDE.md`).
   - Slugify the description: lowercase, hyphen-separated, concise (3–6 words max). Drop filler words.
   - If the arguments are a ticket link, fetch it first (step 6) and build the slug from its ID and title, following the repo's ticket-in-branch convention.
   - Example: arguments `"add agent onboarding flow"` → `feature/agent-onboarding-flow`.
   - Example: arguments `"fix duplicate charge on retry"` → `fix/duplicate-charge-on-retry`.

4. **Create and check out the branch.** Run `git checkout -b <type>/<slug>`.

5. **Report back.** One line: the branch name created, and confirm it was cut from the current `origin/main` tip.

6. **If the arguments contain a Linear or GitHub issue link, plan the work.** Skip this step entirely when there's no link.
   - Read it: Linear via the Linear MCP `get_issue` (fall back to WebFetch), GitHub via `gh issue view <url> --comments`. Include comments; they usually hold the real detail.
   - **Summary:** at most 4 lines. What's wanted or broken, observed impact, and any constraint the ticket already fixes (deadline, API shape, design link).
   - Then think hard and output a plan under these headings:
     - **Where to look:** specific dirs, files, and symbols that are candidates, with one clause on why each.
     - **How to look:** the concrete greps, file reads, log or DB queries to run in order, and what result confirms or kills each hypothesis.
     - **Shape of the solution:** 1 to 2 candidate approaches, their trade-offs, blast radius, and what tests would cover them.
     - **Open questions:** what needs your decision before implementation starts.
   - Light read-only recon (grep, read, `gh`) is allowed to make the plan concrete. Keep it cheap.
   - End by asking whether to run the plan or revise it.

## Rules

- The branch MUST be cut from a freshly pulled `main`. If step 2 fails, do not proceed to step 4.
- Do not push the branch. Do not create a PR. Those are separate, explicit asks.
- **Never write, edit, or create files in step 6.** `/fresh` ends with a branch and a plan, never with an implementation.
- If the arguments are ambiguous about the type (e.g., "deal with the webhook thing"), pick the most likely prefix and state the assumption in the report — the user can correct it before any commits land.
- If the repo's default branch isn't `main` (e.g., `master`, `develop`), use that instead and note it in the report.
