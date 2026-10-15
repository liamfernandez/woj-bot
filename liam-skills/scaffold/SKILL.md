---
description: Scaffold the file tree, signatures, imports, types, and module wiring for a feature WITHOUT implementing logic — method bodies are pseudocode comments for manual fill-in. Use when the user invokes /scaffold (with or without an inline prompt), or asks to "scaffold", "stub out", or "skeleton" a feature, typically right after a planning step.
---

# Scaffold

Generate the skeleton of a feature so the user can open their editor and fill in each method body by hand. Every file exists, every signature is correct, every import resolves — only logic is missing.

## Invocation

| Form | Source of truth |
|------|-----------------|
| `/scaffold` (no args) | Full prior conversation — usually a plan just produced. Treat that plan as the spec. |
| `/scaffold <prompt>` | The inline prompt is the primary directive; prior conversation is supporting context. If they conflict, the inline prompt wins. |

If neither a plan nor an inline prompt is present, stop and ask the user what to scaffold.

## What to STUB

Method, function, and class bodies. Replace each body with a comment block describing:

- What the method must do
- Inputs it receives
- Outputs it returns
- Edge cases or dependencies the plan surfaced

If the language requires a return statement to compile/parse, use the most minimal placeholder under the comment block: `return None`, `return nil`, `raise NotImplementedError`, `throw new Error("not implemented")`, `todo!()`, etc.

No real logic. No "while I'm here" partial implementations. Pseudocode comments only.

## What to FULLY IMPLEMENT

Real, working code — not stubs:

- File names, directory placement, the overall tree
- Class declarations
- Method/function signatures: parameter names, type annotations, return type annotations
- Imports and exports
- Type definitions, interfaces, enums, constants
- Config files (if the plan calls for them)
- **Module wiring** — index registrations, router additions, registry entries, dependency injection bindings, etc.

When the user opens their editor, the project should compile/parse and the only work left should be replacing pseudocode comments with logic.

## Match Project Conventions

Language-agnostic. Infer the target language(s) from the project (existing files, build configs, the plan). Then match the project's:

- File naming (`snake_case.rb`, `kebab-case.ts`, `PascalCase.cs`, etc.)
- Directory layout
- Casing for classes, methods, constants
- Import style (named vs default, relative vs absolute paths)

Read a few neighboring files before writing — do not impose a generic "best practice" if it diverges from the project's existing style.

## Confirmation

| Number of files | Behavior |
|-----------------|----------|
| ≤ 5 | Create immediately. No confirmation. |
| > 5 | First print the planned file tree with a one-line description per file, then ask for confirmation before writing anything. |

## Constraints

- **No test files.** Code stubs only. If the plan mentions tests, note them in the summary but do not generate them.
- **Do not run, build, lint, or execute** anything. The skill ends when files are written.
- **Do not commit or push.** Just write files.

## Output

After writing, print a compact summary: each file created and a one-line note on what's left to implement in it. Example:

```
Created:
- app/services/proof_of_personhood.rb — implement #verify (call KYC provider, cache result by user_id)
- app/jobs/personhood_check_job.rb — implement #perform (enqueue verify, retry on transient failure)
- app/services/task_engine/tasks/proof_of_personhood_task.rb — implement #run (gate on PoP service, emit completion event)
- config/initializers/task_engine.rb — wired (task registered)
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing real logic in a method body | Stop. Replace with a pseudocode comment + minimal placeholder. |
| Generating test files | Stop. Scaffold is code stubs only. |
| Inventing a generic structure that ignores project layout | Re-read neighboring files; match casing, paths, import style. |
| Skipping module wiring (e.g. forgetting to register the new task in an index) | Wiring is FULLY implemented, not stubbed. |
| Writing >5 files without confirming first | Always print the tree and ask. |
| Running build / tests after scaffolding | The skill ends when files are written. Do not execute. |
| Asking the user "what should I scaffold?" when a plan is in the prior conversation | The plan IS the spec. Use it. Only ask if both prior context AND inline prompt are absent. |
