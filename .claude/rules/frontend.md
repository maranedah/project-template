---
globs: ["frontend/**"]
description: Frontend conventions — auto-applied when frontend files are touched.
---

# Frontend rules

- Atomic placement: no state & no child components → `atoms/`; composes atoms with
  local form/UI state → `molecules/`; fetches data → `organisms/`; page chrome →
  `templates/`; wiring → `pages/`. A component imports only from layers below it.
- ALL server calls go through `src/api/client.ts`; `src/api/types.ts` mirrors the
  backend contract 1:1 and changes only with the backend, in the same task.
- Every interactive element gets a `data-testid` (e2e page objects depend on them).
- UI budget: visible feedback <100 ms, result <1 s (<300 ms when possible) —
  docs/03-technical/06-constraints/01-budgets.md. Disable controls while busy;
  show backend `detail` errors via role="alert".
- Deps: exact versions in package.json (npm install --save-exact); lockfile committed.
