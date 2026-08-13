#!/usr/bin/env python3
"""Validate the docs/ tree. Run from the repo root: python docs/lint_docs.py

Checks, ordered by the pain each prevents:
  ERROR  missing required folder/file        -> broken CLAUDE.md router links
  ERROR  bad task/feature front-matter       -> --backlog sorting silently wrong
  ERROR  bad tracking CSV header             -> appended datapoints unreadable later
  WARN   doc exceeds the 120-line budget     -> token waste on every routed read
  WARN   file at docs/ top level             -> "nothing new at the top level" rule

--backlog: print planned/current work sorted by (complexity, manual_intervention,
estimate_hours) ascending — quick wins first — for docs/02-planning/00-index.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent
LINE_BUDGET = 120

REQUIRED = [
    "00-index.md",
    "01-project-definition/01-problem-and-scope.md",
    "01-project-definition/02-workflows.md",
    "01-project-definition/03-success-criteria.md",
    "01-project-definition/04-kpi-definitions.md",
    "01-project-definition/05-decision-log.md",
    "02-planning/00-index.md",
    "02-planning/tasks/TEMPLATE.md",
    "02-planning/features/TEMPLATE.md",
    "02-planning/devlog/index.md",
    "02-planning/devlog/TEMPLATE.md",
    "02-planning/weekly-updates/index.md",
    "02-planning/weekly-updates/TEMPLATE.html",
    "02-planning/tracking/kpis.csv",
    "02-planning/tracking/workflow-runs.csv",
    "03-technical/01-project-organization/01-repo-layout.md",
    "03-technical/02-solution-definition/01-overview.md",
    "03-technical/03-data-definition/01-schema.md",
    "03-technical/04-architecture-definition/01-cloud-stack.md",
    "03-technical/05-deployment/01-cicd.md",
    "03-technical/06-constraints/01-budgets.md",
    "03-technical/07-e2e-validation/01-selenium.md",
    "03-technical/08-security/01-secrets.md",
    "03-technical/09-marketing/01-business-plan.md",
    "04-findings/00-index.md",
    "04-findings/TEMPLATE.md",
    "05-guidelines/01-development.md",
    "06-how-to-use/01-user-manual.md",
]

CSV_HEADERS = {
    "02-planning/tracking/kpis.csv": "date,kpi,value,unit,source,notes",
    "02-planning/tracking/workflow-runs.csv": "date,workflow,outcome,duration_min,evidence,notes",
}

TASK_FIELDS = {"id", "title", "status", "complexity", "manual_intervention", "estimate_hours"}
MANUAL_ORDER = {"none": 0, "low": 1, "medium": 2, "high": 3}
TOP_LEVEL_OK = {"00-index.md", "lint_docs.py"}


def front_matter(path: Path) -> dict[str, str]:
    lines = path.read_text().splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fm: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fm
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.split("#")[0].strip()
    return {}


def work_items() -> list[dict[str, str]]:
    items = []
    for folder in ("tasks/current", "tasks/done", "features/current", "features/done", "features/planned"):
        base = DOCS / "02-planning" / folder
        if base.is_dir():
            for path in sorted(base.glob("*.md")):
                items.append(front_matter(path) | {"_path": str(path.relative_to(DOCS))})
    return items


def lint() -> int:
    errors, warnings = [], []

    for rel in REQUIRED:
        if not (DOCS / rel).exists():
            errors.append(f"missing required file: docs/{rel}")

    for rel, header in CSV_HEADERS.items():
        path = DOCS / rel
        if path.exists() and path.read_text().splitlines()[:1] != [header]:
            errors.append(f"bad CSV header in docs/{rel} (expected: {header})")

    for item in work_items():
        missing = TASK_FIELDS - item.keys()
        if missing:
            errors.append(f"{item['_path']}: front-matter missing {sorted(missing)}")
        elif item["manual_intervention"] not in MANUAL_ORDER:
            errors.append(f"{item['_path']}: manual_intervention must be one of {list(MANUAL_ORDER)}")

    for path in DOCS.rglob("*.md"):
        if path.name != "TEMPLATE.md" and len(path.read_text().splitlines()) > LINE_BUDGET:
            warnings.append(f"docs/{path.relative_to(DOCS)} exceeds the {LINE_BUDGET}-line budget")

    for path in DOCS.iterdir():
        if path.is_file() and path.name not in TOP_LEVEL_OK:
            warnings.append(f"docs/{path.name}: nothing new at the top level of docs/")

    for msg in errors:
        print(f"ERROR  {msg}")
    for msg in warnings:
        print(f"WARN   {msg}")
    print(f"docs lint: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


def backlog() -> int:
    rows = [i for i in work_items() if i.get("status") in ("planned", "current") and TASK_FIELDS <= i.keys()]
    rows.sort(key=lambda i: (int(i["complexity"]), MANUAL_ORDER[i["manual_intervention"]], float(i["estimate_hours"])))
    print("| id | title | complexity | manual | est. hours |")
    print("|---|---|---|---|---|")
    for item in rows:
        print(f"| {item['id']} | {item['title']} | {item['complexity']} | {item['manual_intervention']} | {item['estimate_hours']} |")
    return 0


if __name__ == "__main__":
    sys.exit(backlog() if "--backlog" in sys.argv else lint())
