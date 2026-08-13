# Findings

Read this when: before debugging (known bugs), before optimizing (existing numbers),
before relying on an external API (known limits).

- **Benchmarks** → [benchmarks/](benchmarks/) — one file per constraint
  (disk, memory, time, ui_response_time, accuracy, cost); each run appends a dated
  section. Summarize the latest number per file in the table below.
- **Everything else** (api-limit, lib-limit, bug, incident) → numbered
  `NNNN-slug.md` from [TEMPLATE.md](TEMPLATE.md); one row here per entry.
- Cite findings by id (`F-0001`) from code comments and docs.

## Entries

| Id | Date | Category | Result (one line) |
|---|---|---|---|
| [F-0001](0001-no-hot-reload-in-compose.md) | 2026-08-13 | bug | Hot reload in compose kills in-flight work and corrupts measurements — never enable it |

## Latest benchmark numbers

| Constraint | Latest | Date |
|---|---|---|
| <!-- FILL as benchmarks land --> | | |
