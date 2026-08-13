# E2E validation (Selenium)

Read this when: writing or debugging a UI end-to-end test.

## Run

```bash
make up && make e2e        # parallel (pytest-xdist, one Chrome per worker)
E2E_HEADLESS=0 make e2e    # watch the browser
E2E_BASE_URL=https://<deployed-url> make e2e   # against an environment (CI does this)
```

## Pattern

- Suite lives in `frontend/e2e/`; page objects in `frontend/e2e/pages/` — tests never
  touch selectors directly.
- Tests are `unittest.TestCase` classes; each gets its own driver (xdist-safe).
- Every test screenshots at its end (pass or fail) → `frontend/e2e/screenshots/` —
  these are the artifacts the UI reviewer analyzes (see
  [../../05-guidelines/02-review.md](../../05-guidelines/02-review.md)).
- Keep tests independent (unique data per test) so parallel order never matters.
  Perf-measuring tests run sequentially: `pytest -n 0 -k perf`.

## Adding a flow

1. Add/extend a page object with the new interactions.
2. One test class per workflow (name it after the W-NN id).
3. Assert user-visible outcomes (text on screen), not implementation details.
