# Documentation index

**Rules:** every folder is numbered; new documents go inside the matching folder —
**nothing new at the top level of `docs/`**. Every doc opens with a one-line
"Read this when…" header. Line budget per doc: 120. `python docs/lint_docs.py` enforces this.

| Folder | Purpose |
|---|---|
| [01-project-definition/](01-project-definition/) | Problem, workflows (W-NN), success criteria, KPI definitions (KPI-NN), decision log |
| [02-planning/](02-planning/) | Tasks, features, backlog, devlog, weekly updates, KPI/workflow tracking |
| [03-technical/](03-technical/) | 01 organization · 02 solution · 03 data · 04 architecture · 05 deployment · 06 constraints · 07 e2e · 08 security · 09 marketing |
| [04-findings/](04-findings/) | Benchmarks (per constraint), API/library limitations, bugs to avoid |
| [05-guidelines/](05-guidelines/) | Development, review, and writing guidelines |
| [06-how-to-use/](06-how-to-use/) | End-user manual |

## Load-bearing docs (parsed by code or CI — do not restructure casually)

| File | Consumer |
|---|---|
| `02-planning/tracking/*.csv` | append-only; headers checked by `lint_docs.py` |
| `02-planning/{tasks,features}/*/*.md` front-matter | `lint_docs.py --backlog` sorting |
| `../.env.example` | humans + compose; SSOT for env vars |
| `../Makefile` | SSOT for commands; CI mirrors it |

## Per-folder file map

- **01-project-definition**: 01 problem-and-scope · 02 workflows · 03 success-criteria · 04 kpi-definitions · 05 decision-log
- **02-planning**: 00-index (backlog) · tasks/{TEMPLATE,current,done} · features/{TEMPLATE,current,done,planned} · devlog/ · weekly-updates/ · tracking/
- **03-technical/01-project-organization**: 01 repo-layout · 02 connectors · 03 env-vars
- **03-technical/02-solution-definition**: 01 overview (sequence diagrams) · 02 algorithms
- **03-technical/03-data-definition**: 01 schema · 02 validation-rules · 03 data-licensing
- **03-technical/04-architecture-definition**: 01 cloud-stack · 02 connections · 03 observability · diagrams/
- **03-technical/05-deployment**: 01 cicd · 02 terraform · 03 backup-restore
- **03-technical/06-constraints**: 01 budgets
- **03-technical/07-e2e-validation**: 01 selenium · 02 screen-capture
- **03-technical/08-security**: 01 secrets · 02 access
- **03-technical/09-marketing**: 01 business-plan · 02 videos
- **04-findings**: 00-index · TEMPLATE · NNNN-slug entries · benchmarks/{disk,memory,time,ui_response_time,accuracy,cost}
- **05-guidelines**: 01 development · 02 review · 03 writing
