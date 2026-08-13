# Template initialization checklist

Run through this once, top to bottom, right after `cp -r project-template <name>`.

## 1. Rename the project token

```bash
grep -rl PROJECT_NAME . --exclude-dir=node_modules --exclude-dir=.git | xargs sed -i 's/PROJECT_NAME/myproj/g'
```

Token locations (the find-replace covers all of them):

| File | What it names |
|---|---|
| `README.md`, `.claude/CLAUDE.md`, `.env.example` | Title / router / config headers |
| `backend/pyproject.toml` | Package distribution name (`PROJECT_NAME-backend`) |
| `backend/app/infrastructure/api/app.py` | FastAPI title |
| `frontend/index.html`, `frontend/src/components/templates/MainLayout.tsx` | Page title / header |
| `terraform/variables.tf` | Default resource prefix |
| `docs/02-planning/weekly-updates/TEMPLATE.html` | Report header |

The backend import package is `app` — code needs no renames. `frontend/package.json`
uses the lowercase `project-name-frontend` (npm forbids uppercase); rename it by hand
if you care about the npm name.

## 2. Verify zero leftovers

```bash
grep -r PROJECT_NAME . --exclude-dir=node_modules --exclude-dir=.git --exclude=INIT.md
# must print nothing
```

## 3. Pick ports (incremental, never default)

Each project takes the next free +10 increment so stacks can run side by side.
Check what's taken: `docker ps --format '{{.Ports}}'` and other projects' `.env` files.

```bash
cp .env.example .env
# Edit APP_BACKEND_PORT (base 8100), APP_FRONTEND_PORT (base 3100), APP_DB_PORT (base 5532)
```

## 4. Git

```bash
git init -b main && git add -A && git commit -m "Bootstrap from project-template"
git checkout -b develop     # develop is the working default branch
```

## 5. GitHub

```bash
gh repo create <owner>/<name> --private --source=. --push
git push -u origin develop
gh repo edit --default-branch develop
# Secrets (full list + rationale: docs/03-technical/08-security/01-secrets.md)
gh secret set GCP_PROJECT_ID_DEV
gh secret set GCP_PROJECT_ID_PROD
gh secret set GCP_WIF_PROVIDER          # workload identity federation, keyless deploys
gh secret set GCP_WIF_SERVICE_ACCOUNT
# Protect main: PRs only (from develop), checks must pass, no direct push
gh api -X PUT "repos/{owner}/{repo}/branches/main/protection" --input - <<'EOF'
{
  "required_status_checks": {"strict": true, "contexts": ["checks / checks"]},
  "enforce_admins": true,
  "required_pull_request_reviews": {"required_approving_review_count": 0},
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
```

## 6. Verify the skeleton runs

```bash
make verify
```

## 7. Fill the project definition

`docs/01-project-definition/` is the only docs folder that MUST be filled before the
first task: problem, workflows (W-NN), success criteria, KPI definitions (KPI-NN).

## 8. Worker: keep or drop

Long-running/retryable jobs (>30 s)? Uncomment the `worker` service in
`docker-compose.yml` (migration `0002_jobs` already ships). Otherwise leave it.
When to enable: `docs/03-technical/04-architecture-definition/01-cloud-stack.md`.

## 9. First devlog entry

Copy `docs/02-planning/devlog/TEMPLATE.md` → `YYYY-MM-genesis.md`; add it to
`devlog/index.md`.

## 10. Replace the example slice

The `Item` entity (backend + frontend + e2e) is the reference implementation of the
full pattern. Replace it with your first real entity in your first task — do not keep
both. Delete this file when done.
