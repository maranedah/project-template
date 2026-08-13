# syntax=docker/dockerfile:1
# ── Migrations image: apply-only, tiny (alembic + driver, no app code) ─────────
# `alembic revision --autogenerate` runs from backend/.venv on the host (needs app
# models); this image only ever applies. CI paths-filters on backend/db/** so it
# rebuilds only when migrations change.
# Base digest-pinned: the digest freezes the exact rebuild we tested with; bump it
# deliberately together with a `make verify` run.
FROM python:3.12-slim@sha256:229a2c5bfa27522db7815ea81f9bed70af17ccb9de9fc7ad142b1877b5830d36

WORKDIR /migrations

# Dependency layer isolated: editing migrations never re-runs pip install.
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY alembic.ini .
COPY migrations/ migrations/

ENTRYPOINT ["alembic"]
CMD ["upgrade", "head"]
