# Planning

Read this when: picking the next piece of work or filing a new task/feature.

## How planning works

- **Tasks** (`tasks/`): units of work. Copy `tasks/TEMPLATE.md` → `current/T-NNNN-slug.md`;
  move to `done/` on completion (fill `done:` date and `## Result`).
- **Features** (`features/`): user-visible capabilities, linked to a KPI and a workflow.
  Live in `planned/` → `current/` → `done/`.
- Front-matter fields (`complexity`, `manual_intervention`, `estimate_hours`) drive the
  backlog sort — quick wins first.
- **Devlog** (`devlog/`): monthly narrative history. **Weekly updates** (`weekly-updates/`):
  stakeholder-facing HTML snapshots.
- **Tracking** (`tracking/`): append-only CSVs for KPI datapoints and workflow runs
  (ids from [../01-project-definition/](../01-project-definition/)).

## Backlog

Regenerate with `python docs/lint_docs.py --backlog` and paste below.

| id | title | complexity | manual | est. hours |
|---|---|---|---|---|
<!-- FILL: paste --backlog output -->
