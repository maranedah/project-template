# Repo layout

Read this when: adding code and unsure where it goes.

## Topology

`docker-compose.yml` is the SSOT: `db` → `migrate` (applies alembic, own image at
`backend/db/`) → `backend` → `frontend`; `worker` ships commented out. **No hot
reload** — rationale: [F-0001](../../04-findings/0001-no-hot-reload-in-compose.md).
Apply code changes with `docker compose restart <svc>`.

## Backend — hexagonal (`backend/app/`)

| Layer | Contains | May import |
|---|---|---|
| `domain/` | models (frozen dataclasses), ports (Protocols) | nothing internal |
| `application/` | use cases (services) | domain |
| `infrastructure/` | FastAPI (`api/`), SQLAlchemy (`persistence/`), external adapters | application, domain |
| `composition.py`, `worker.py` | wiring roots — the ONLY modules that assemble adapters | everything |

Enforced by import-linter (`make lint`). Deps: `requirements*.txt` with **exact `==`
pins**; `pyproject.toml` packs the code as the `app` package (`pip install -e .`) so
imports never depend on the working directory. Tests: `unittest.TestCase` classes in
`backend/tests/`, parallel via `pytest -n auto`.

## Frontend — atomic design (`frontend/src/`)

`components/atoms → molecules → organisms → templates → pages`; a component may only
import from layers below it. `api/client.ts` + `api/types.ts` mirror the backend
contract 1:1 — change `types.ts` only when the backend contract changes, in the same
task. Placement rule: no state + no children → atom · composes atoms → molecule ·
fetches data → organism · page chrome → template.

## Build-speed rules

Dockerfiles are multi-stage with digest-pinned bases and dependency layers isolated
from code layers (editing code never re-runs `pip install`/`npm ci`). Keep it that
way; measure any change with `time docker compose build` twice and file the numbers
in [benchmarks/time.md](../../04-findings/benchmarks/time.md).
