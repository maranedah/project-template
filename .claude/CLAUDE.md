# PROJECT_NAME

<!-- FILL: one line — what this project does. -->

## Golden rules

1. Never restate documented facts — link them. SSOTs: `.env.example` (env vars),
   `docker-compose.yml` (topology), `Makefile` (commands), `docs/04-findings/` (rationale),
   `frontend/src/api/types.ts` (API contract).
2. Every task: own `feat/T-NNNN-slug` branch off `develop`, finished via `/finish-task`
   (tests ∥ + build + e2e + minimal permissions + green Actions run). Never push to `main`.
3. Every benchmark/measurement → `docs/04-findings/benchmarks/<constraint>.md`.
   Every optimization compares ≥2 approaches there before shipping.
4. Tests are `unittest.TestCase` classes; run `make test` (pytest -n auto, parallel).
5. Fit model to task: spawn cheap subagents for simple subtasks; give each only the
   task file's "Context docs" list (see docs/05-guidelines/01-development.md).

## Task router — read ONLY the listed docs

| Task | Read first |
|---|---|
| Add backend feature | docs/03-technical/01-project-organization/01-repo-layout.md + the task file in docs/02-planning/tasks/current/ |
| Add data entity | docs/03-technical/03-data-definition/01-schema.md + 02-validation-rules.md |
| Fix bug | backend/var/log/*-errors.log + docs/04-findings/00-index.md (known bugs) |
| Debug an error | backend/var/log/*-errors.log first — timestamped, errors only |
| Frontend/UI work | 01-repo-layout.md + docs/03-technical/06-constraints/01-budgets.md |
| Connector work | docs/03-technical/01-project-organization/02-connectors.md |
| Deploy / CI change | docs/03-technical/05-deployment/01-cicd.md (+ 02-terraform.md if infra) |
| Benchmark / optimize | docs/03-technical/06-constraints/01-budgets.md + docs/04-findings/benchmarks/ |
| Plan new work | docs/02-planning/00-index.md |
| Write devlog | /write-devlog |
| Weekly update | /weekly-update |
| Reel (show a feature/mechanic) | .claude/skills/feature-reel/SKILL.md |
| Trailer / narrated video | .claude/skills/marketing-video/SKILL.md |

Never read `docs/02-planning/devlog/` or `docs/03-technical/09-marketing/` for coding
tasks — largest prose, zero engineering signal.

## Commands

`make up | down | test | lint | e2e | build | verify` — defined once, in the Makefile.
Slash: `/finish-task` `/review-pr` `/write-devlog` `/weekly-update`.
