# Environment variables

Read this when: adding a new env var or wondering what one does.

**SSOT is [`.env.example`](../../../.env.example)** — every var is defined and
commented there, grouped by concern (Core / Ports / Database / Worker / Storage /
Connectors / E2E / Compose-only). This doc only records the rules:

- Prefix everything the backend reads with `APP_` (parsed by pydantic-settings in
  `backend/app/settings.py`; a new var needs a field there).
- Mark secrets with a `# SECRET` comment; secrets never get committed defaults.
- Ports are incremental per project, never 8000/3000 — see `.claude/INIT.md` step 3.
- Adding a var = add to `.env.example` + `settings.py` + (if a connector) a row in
  [02-connectors.md](02-connectors.md). Nothing else.
