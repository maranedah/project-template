# Secrets management

Read this when: adding a secret, or setting up a new repo/environment.

## Rules

- Secrets live in `.env` (local, gitignored) and **GCP Secret Manager** (deployed) —
  never in code, compose files, tfvars, or CI logs. `.env.example` documents the
  names with `# SECRET` and empty values.
- CI reads GitHub Secrets; deploys authenticate keylessly via Workload Identity
  Federation (no service-account key files, ever — don't create `*-sa-key.json`).
- Cloud Run gets secrets as Secret Manager references in the terraform modules, not
  plaintext env.

## Initial GitHub setup (run once per repo)

```bash
gh secret set GCP_PROJECT_ID_DEV
gh secret set GCP_PROJECT_ID_PROD
gh secret set GCP_WIF_PROVIDER           # projects/N/locations/global/workloadIdentityPools/...
gh secret set GCP_WIF_SERVICE_ACCOUNT    # deployer@<project>.iam.gserviceaccount.com
# FILL: one gh secret set per connector secret in .env.example
```

Branch protection commands live in `.claude/INIT.md` step 5 — don't duplicate here.

## Rotation

<!-- FILL: rotation period per secret and who owns it. -->
