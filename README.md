# PROJECT_NAME

<!-- FILL: one-line description of what this project does and for whom. -->

Bootstrapped from `project-template`. If `PROJECT_NAME` still appears anywhere in this
repo, the template has not been initialized — follow [.claude/INIT.md](.claude/INIT.md) first.

## Quickstart

```bash
cp .env.example .env      # fill secrets, pick ports (.claude/INIT.md step 3)
make verify               # tests + build + full stack + e2e
make up                   # start the stack
```

Backend: http://localhost:${APP_BACKEND_PORT} · Frontend: http://localhost:${APP_FRONTEND_PORT}

## Where everything is

| Path | Purpose |
|---|---|
| [.claude/CLAUDE.md](.claude/CLAUDE.md) | Task router — which docs to read for which task |
| [docs/00-index.md](docs/00-index.md) | Full documentation map |
| [docs/01-project-definition/](docs/01-project-definition/) | Problem, workflows, success criteria, KPIs |
| [backend/](backend/) | FastAPI, hexagonal (`app/domain` → `app/application` → `app/infrastructure`); runtime logs in `backend/var/log/` |
| [frontend/](frontend/) | React + Vite, atomic design; Selenium UI suite in `frontend/e2e/` |
| [Makefile](Makefile) | Canonical commands — the only place commands are defined |

## Template conventions (non-negotiable)

- Exact-pin dependencies (`==`) in `requirements*.txt`; `pyproject.toml` packs the backend as a library.
- Tests are `unittest.TestCase` classes, run in parallel via `pytest -n auto`.
- No hot reload in docker compose — see [docs/04-findings/0001-no-hot-reload-in-compose.md](docs/04-findings/0001-no-hot-reload-in-compose.md).
- Every task: own `feat/T-NNNN-slug` branch off `develop`; `main` only receives PRs from `develop`.
- Every datum has a `source`; every benchmark lands in [docs/04-findings/benchmarks/](docs/04-findings/benchmarks/).
# project-template
