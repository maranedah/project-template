---
globs: ["backend/**"]
description: Backend conventions — auto-applied when backend files are touched.
---

# Backend rules

- Hexagonal, lint-enforced (`make lint`): `domain` imports nothing internal;
  `application` imports domain only; `infrastructure` implements `domain/ports.py`;
  ONLY `composition.py`/`worker.py` assemble adapters.
- New adapter = implement a Protocol from `domain/ports.py` + provide the offline
  twin (InMemory/Null) next to it. Tests use the twin.
- Every persisted datum has a `source` value: `file:` | `api:` | `url:` | `manual:`.
- Deps: exact `==` pins in `requirements*.txt`; never `>=`. Bump + `make verify` in
  the same commit. Don't add deps to `pyproject.toml`.
- Tests: `unittest.TestCase` classes, offline by construction, parallel-safe
  (no shared state, no fixed ports/files). Run `make test`.
- Endpoints: schemas inline in `routes.py`, mirrored in `frontend/src/api/types.ts`
  in the same task. Domain errors raise `ValidationError` → 422 handler.
- DB access: batch queries, no N+1 (reviewers check); migrations are handwritten,
  numbered `NNNN_slug.py` in `backend/db/migrations/versions/`.
- New service = its own `logging.yaml` copy with `<service>-errors.log` filename.
