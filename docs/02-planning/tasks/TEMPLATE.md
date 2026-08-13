---
id: T-0000
title: <!-- FILL: short imperative title -->
status: current          # current | done
complexity: 3            # 1 trivial edit … 5 architectural change
manual_intervention: low # none | low | medium | high — human steps required
estimate_hours: 4
branch: feat/T-0000-slug
created: YYYY-MM-DD
done:                    # fill when moving to done/
---

## Goal

<!-- FILL: 1-2 lines. What is true when this task is done. -->

## Context docs

<!-- FILL: the ONLY docs needed to work this task. Subagents get exactly this list.
- docs/03-technical/01-project-organization/01-repo-layout.md
-->

## Steps

<!-- FILL: numbered, small. -->

## Validation gate

- [ ] `make test` passes (parallel)
- [ ] `make build` clean
- [ ] `make e2e` green (UI workflow exercised)
- [ ] Permissions/secrets touched are minimal for the change
- [ ] Perf-relevant? benchmark filed in docs/04-findings/benchmarks/
- [ ] Branch pushed → `gh run watch` until the Actions run is green

## Result

<!-- FILL at completion: what shipped, link PR. If a tracked workflow was exercised,
append a line to ../tracking/workflow-runs.csv. -->
