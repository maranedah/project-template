# Development guidelines

Read this when: starting any task, or spawning subagents.

## Subagents

- Fit the model to the complexity: cheap/fast models for mechanical edits, lookups,
  and file generation; mid-tier for scoped features; top-tier only for architecture
  and hard debugging.
- Parallelizable simple subtasks → spawn subagents; give each ONLY the task file's
  "Context docs" list, never the whole tree.
- Deferred: tinytroupe persona-based UI validation (optimize the library first).

## Branching & completion

- One task = one `feat/T-NNNN-slug` branch off `develop`. Never push to `main`.
- A task is done when its Validation gate passes (tasks/TEMPLATE.md): tests ∥ +
  container build + e2e UI + minimal-permissions check + **green Actions run**
  (`gh run watch`). `/finish-task` runs the gate.

## Ship optimized

- Every task ships optimized against the budgets
  ([../03-technical/06-constraints/01-budgets.md](../03-technical/06-constraints/01-budgets.md)).
- Every optimization benchmarks ≥2 approaches and files the numbers in
  [../04-findings/benchmarks/](../04-findings/benchmarks/) before the winner ships.

## Offline mode (data-science projects — always)

- **Sample before you extract**: full extraction is slow and often paid. Validate the
  entire pipeline (parse → validate → store → consume) against a small offline sample
  first; run the full extraction only once the pipeline passes on the sample.
- Offline is the default mode; the app and tests run from local data/fixtures.
- The FIRST online connection creates the backup that offline mode uses
  ([backup-restore](../03-technical/05-deployment/03-backup-restore.md)) — the sample
  above is its first slice.
- Every connector has a documented offline-update command
  ([connectors](../03-technical/01-project-organization/02-connectors.md)).
- Code seam: adapter twins (Sql/InMemory, gcs/local, real/Null) selected by env.
