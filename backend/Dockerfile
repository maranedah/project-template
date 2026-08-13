# syntax=docker/dockerfile:1
# ── Backend image (API; the worker reuses it via a compose `command:` override) ──
# Build-speed rules (docs/03-technical/01-project-organization/01-repo-layout.md):
#   - Base digest-pinned: freezes the exact rebuild we tested with; bump deliberately.
#   - Dependency layer isolated in a builder stage: editing app code never re-runs pip.
#   - pip cache mount: re-pinning a single dep doesn't re-download the rest.
# If the worker grows heavy deps (GPU/ML), split a Dockerfile.worker instead of
# fattening this image.
FROM python:3.12-slim@sha256:229a2c5bfa27522db7815ea81f9bed70af17ccb9de9fc7ad142b1877b5830d36 AS builder
WORKDIR /srv
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m venv /venv && /venv/bin/pip install -r requirements.txt

FROM python:3.12-slim@sha256:229a2c5bfa27522db7815ea81f9bed70af17ccb9de9fc7ad142b1877b5830d36
WORKDIR /srv
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

COPY pyproject.toml logging.yaml ./
COPY app/ app/
# Install the code as the `app` library (consistent imports, no sys.path games).
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-deps -e .

# Non-root, uid 1000 = typical host user, so the bind-mounted var/log stays writable.
RUN useradd --uid 1000 --create-home appuser && mkdir -p var/log && chown -R appuser /srv
USER appuser

# No --reload anywhere: docs/04-findings/0001-no-hot-reload-in-compose.md
CMD ["uvicorn", "--factory", "app.composition:build_api", "--host", "0.0.0.0", "--port", "8000", "--log-config", "logging.yaml"]
