# /review-pr — fresh-context PR validation

Review the PR given as argument (or the current branch's diff vs develop).
**Spawn three subagents** — each gets ONLY the diff and its persona brief below, no
implementation context from this session. Full brief: docs/05-guidelines/02-review.md.

1. **Architecture enforcer**: hexagonal violations linters can't see (domain logic
   leaked into adapters, use cases doing I/O, wiring outside composition roots),
   contract drift between backend schemas and frontend/src/api/types.ts, dead code,
   duplication vs existing utilities. Non-negotiables: no `>=` pins, no hot reload,
   no missing `source` on new data.
2. **Optimization enforcer**: check the diff against
   docs/03-technical/06-constraints/01-budgets.md — N+1 queries, unbatched I/O,
   missing pagination, oversized outputs. Claimed optimizations must have a
   benchmarks/ entry with ≥2 approaches; verify the numbers support the claim.
3. **UI enforcer** (only if frontend changed): `make up`, exercise the changed flows,
   capture screenshots (docs/03-technical/07-e2e-validation/02-screen-capture.md) and
   judge the rendered UI: layout breakage, loading feedback, error states, budget
   compliance, consistency with existing screens.

Collect the three reports, deduplicate, present findings ranked by severity with
file:line. Blocking findings → request changes; recurring traps → file in
docs/04-findings/.
