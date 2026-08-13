# Benchmarks: Memory

Read this when: measuring this constraint or checking existing numbers. Append-only —
newest section on top. Budgets live in
[../../03-technical/06-constraints/01-budgets.md](../../03-technical/06-constraints/01-budgets.md).

How to measure: docker stats --no-stream · /usr/bin/time -v <cmd> (Maximum resident set size)

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
