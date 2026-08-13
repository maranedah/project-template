# Constraint budgets

Read this when: optimizing, sizing infra, or reviewing performance.

Every measurement lands in [../../04-findings/benchmarks/](../../04-findings/benchmarks/)
(one file per constraint, dated sections). This doc holds only the targets.

| Constraint | Budget | Measured in |
|---|---|---|
| UI response to a click | **<1 s always, <300 ms when possible** | benchmarks/ui_response_time.md |
| Backend endpoint p95 | <!-- FILL: e.g. 200 ms --> | benchmarks/time.md |
| DB requests per endpoint | minimal — **no N+1**; joins/batch over loops | benchmarks/time.md |
| Backend memory (container) | <!-- FILL: e.g. 512 MB --> | benchmarks/memory.md |
| Disk / file output size | <!-- FILL: per artifact type --> | benchmarks/disk.md |
| Docker image build (warm) | <!-- FILL: e.g. <30 s --> | benchmarks/time.md |
| Monthly cloud cost | <!-- FILL --> | benchmarks/cost.md |
| Accuracy (if ML/data) | <!-- FILL --> | benchmarks/accuracy.md |

## Optimization guidelines

- Optimize on evidence: benchmark ≥2 approaches, file both numbers, ship the winner.
- Frontend: paginate lists, debounce inputs, lazy-load routes; show feedback <100 ms
  even when the operation is slower (optimistic UI / spinners).
- Backend: batch DB access (the N+1 check is part of review), stream large outputs.
- Images: build measured with `time docker compose build` (cold + warm).

## How to build images

`make build` (all) or `docker compose build <service>` (one). Layer rules in
[01-project-organization/01-repo-layout.md](../01-project-organization/01-repo-layout.md) §build-speed.
