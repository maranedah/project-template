# /finish-task — run the task validation gate

Run the full gate for the current task branch. Stop at the first failure, fix, rerun.

1. Confirm you're on the task's `feat/T-NNNN-slug` branch (`git status`), matching
   the task file in docs/02-planning/tasks/current/.
2. `make test` — parallel unit tests green.
3. `make lint` — ruff + import contracts + docs lint green.
4. `make build` — images build clean.
5. `make up && make e2e` — UI workflows green; inspect the new screenshots in
   frontend/e2e/screenshots/ for visual breakage.
6. Minimal-permissions check: list every permission/secret/role the diff touches;
   each must be required by the change (docs/03-technical/08-security/02-access.md).
7. If perf-relevant: confirm the benchmark entry exists in
   docs/04-findings/benchmarks/ (≥2 approaches compared).
8. Commit, push the branch, then `gh run watch` until the Actions run is green —
   the task is NOT done before that.
9. Update the task file: fill `## Result`, set `done:` date, move to tasks/done/.
   If a tracked workflow was exercised, append a line to
   docs/02-planning/tracking/workflow-runs.csv.
10. Open the PR to develop: `gh pr create --base develop`.
