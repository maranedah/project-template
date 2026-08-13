# CI/CD

Read this when: changing workflows, or a deploy behaved unexpectedly.

## Pipeline

`main.yaml` composes reusable workflows (`workflow_call` + `secrets: inherit`):

```
push feat/** ──────► checks ─► build-images                     (validation only)
push develop ──────► checks ─► build-images ─► deploy dev ─► e2e
PR develop→main ───► checks ─► build-images                     (gate for merge)
push main (merge) ─► checks ─► build-images ─► deploy prod ─► e2e
```

- `concurrency: deploy-<branch>` + cancel-in-progress: superseded runs die early.
- Task completion requires the branch's run green: `gh run watch` (see /finish-task).

## Branch model

`feat/T-NNNN-slug` → PR → `develop` (auto-deploys dev) → PR `develop`→`main`
(protected; checks must pass) → merge auto-deploys prod. Direct pushes to `main` are
blocked by branch protection (`.claude/INIT.md` step 5).

## Deploy-time optimization checklist

- Images build with buildx + `cache-from/to: type=gha` — dependency layers hit cache.
- `paths-filter` skips images whose context didn't change (a docs-only push builds
  nothing).
- Keyless GCP auth via Workload Identity Federation — no key files, no key rotation.
- Terraform: `fmt -check` + `validate` gate; plan saved as artifact, applied from it.
- Measure: pipeline duration is a KPI candidate; changes >±20% need a
  [benchmarks/time.md](../../04-findings/benchmarks/time.md) entry.
