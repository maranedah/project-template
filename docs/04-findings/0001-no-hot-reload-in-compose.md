---
id: F-0001
date: 2026-08-13
category: bug
constraint: none
---

## Context

Whether to run `uvicorn --reload` / vite dev watchers inside docker compose.
Inherited from the mp-test project, where reload caused real damage.

## Method

Observed in mp-test production-like runs: a code save while a worker held an active
scraping session triggered the reload watcher, which SIGKILLed the process mid-job.

## Numbers

Not a benchmark — failure modes observed: (1) in-flight jobs killed mid-work, losing
paid external sessions; (2) latency measurements corrupted by watcher CPU noise;
(3) "works until you save a file" bugs that are impossible to reproduce.

## Decision

No hot reload in any compose service. Source is bind-mounted; apply changes with
`docker compose restart <service>`. Fast iteration belongs in unit tests
(`make test`), not in reloading containers. `docker-compose.yml` links this finding.
