# Review guidelines (PR validation)

Read this when: reviewing a PR, or invoking `/review-pr`.

**The reviewer must be a fresh context** — a new model session with no memory of the
implementation, so it can't rationalize the author's choices. `/review-pr` spawns
three personas; each reports findings with file:line and severity:

## 1. Architecture enforcement

Hexagonal layering (imports flow infrastructure → application → domain; wiring only
in composition roots — `make lint` must already pass, the reviewer hunts what linters
can't see: leaked domain logic, adapter logic in use cases, contract drift between
`api/types.ts` and backend schemas), dead code, duplication vs existing utilities.

## 2. Optimization enforcement

Check against budgets ([06-constraints/01-budgets.md](../03-technical/06-constraints/01-budgets.md)):
N+1 queries, unbatched I/O, missing pagination, output sizes. If the PR claims an
optimization: verify the benchmark exists in findings and the numbers support it.

## 3. UI enforcement (analyze the UI directly)

Not a code read: run the stack (`make up`), exercise the changed flows, and judge
the rendered result from screenshots
([screen-capture commands](../03-technical/07-e2e-validation/02-screen-capture.md)):
layout breakage, loading feedback (<100 ms), error states, response-time budget,
visual consistency with existing screens.

## Verdict

Blocking findings → back to the author. No findings → approve. Every finding worth
remembering later (recurring bug shape, library trap) → file in 04-findings.
