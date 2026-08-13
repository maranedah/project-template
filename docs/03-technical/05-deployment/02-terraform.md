# Terraform

Read this when: changing infra or bootstrapping an environment.

## Layout

`terraform/` root (provider, module calls, budget stub) + `backend/`, `frontend/`
modules (Cloud Run v2 service stubs — uncomment and fill on first deploy).

## State & environments

- Remote state in GCS, one bucket per env, injected at init:
  `terraform init -backend-config="bucket=<project>-tf-state-<env>"`.
- Two GCP projects (dev/prod); env selected by branch in CI (`deploy.yml`), by
  `-var env=` locally.

## Commands

```bash
cd terraform
terraform fmt -check && terraform validate
terraform plan -var project_id=<id> -var env=dev -out=tfplan
terraform apply tfplan          # CI applies the saved plan artifact
```

## Secrets

Runtime secrets go through **GCP Secret Manager** referenced from the Cloud Run
modules — never through tfvars→plaintext env (see
[../08-security/01-secrets.md](../08-security/01-secrets.md)).
