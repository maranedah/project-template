# /weekly-update — generate this week's HTML status page

Produce docs/02-planning/weekly-updates/`YYYY-Www.html` (ISO week, e.g. 2026-W33).

1. Gather the week: `git log --since="last monday" --oneline`, tasks moved to
   done/ this week, and the current/ folder for in-progress.
2. KPI snapshot: last row per KPI from docs/02-planning/tracking/kpis.csv, targets
   from docs/01-project-definition/04-kpi-definitions.md.
3. Copy weekly-updates/TEMPLATE.html and fill: Shipped (user-visible phrasing, PR
   links) / In progress (+ expected landing) / KPI snapshot table / Next week (from
   the backlog top: `python docs/lint_docs.py --backlog`) / Risks.
4. Keep it scannable — a stakeholder reads this in 60 seconds. Delete empty sections.
5. Add the file link to weekly-updates/index.md (newest first).
