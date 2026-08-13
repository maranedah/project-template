# Access control (RBAC) & auth

Read this when: adding a protected endpoint, a role, or changing auth settings.

## Roles

Minimal-permissions principle: every role gets the least it needs; every task's
validation gate re-checks this.

| Role | Can | Cannot |
|---|---|---|
| <!-- FILL: e.g. viewer --> | <!-- FILL --> | <!-- FILL --> |
| <!-- FILL: e.g. admin --> | <!-- FILL --> | <!-- FILL --> |

## Auth settings

| | |
|---|---|
| User auth | <!-- FILL: none / Google OIDC / Clave Única / … --> |
| Session | <!-- FILL: cookie/JWT, lifetime --> |
| Service→service | <!-- FILL: Cloud Run IAM invoker / bearer token --> |
| CI→GCP | Workload Identity Federation ([01-secrets.md](01-secrets.md)) |

## Enforcement points

<!-- FILL: where authorization is checked in code (middleware/dependency path)
so reviewers can verify no endpoint bypasses it. -->
