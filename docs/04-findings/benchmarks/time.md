# Benchmarks: Time (backend + build + pipeline)

Read this when: measuring this constraint or checking existing numbers. Append-only —
newest section on top. Budgets live in
[../../03-technical/06-constraints/01-budgets.md](../../03-technical/06-constraints/01-budgets.md).

How to measure: hyperfine '<cmd>' · time docker compose build (cold+warm) · endpoint p95 via repeated curl -w '%{time_total}'

<!-- Entry format — copy for each run:

## YYYY-MM-DD — <what was measured>

**Context**: <why — task id, optimization question>
**Method**: <exact commands, reproducible>

| Approach | Result |
|---|---|
| A | |
| B | |

**Decision**: <which approach ships and why>
-->
