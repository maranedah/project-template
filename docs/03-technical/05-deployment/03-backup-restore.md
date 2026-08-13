# Backup, restore & offline mode

Read this when: setting up backups, restoring after data loss, or refreshing offline data.

## Database

```bash
# Backup (run before risky migrations; scheduled daily in prod)
docker compose exec db pg_dump -U app app | gzip > var/backup-$(date +%F).sql.gz
# gsutil cp var/backup-*.sql.gz gs://<bucket>/db-backups/   # prod: push to GCS
# Restore
gunzip -c var/backup-YYYY-MM-DD.sql.gz | docker compose exec -T db psql -U app app
```

**Restore drill**: after the first real backup, restore it into a scratch DB once and
record the result in [04-findings](../../04-findings/00-index.md). An untested backup
is not a backup.

## Offline mode (data-science rule)

- Offline is the default: tests and dev run from committed fixtures/local data.
- **First online connection creates the backup** — the initial fetch writes the
  offline dataset that everything else uses.
- Every connector documents its offline-update command in
  [01-project-organization/02-connectors.md](../01-project-organization/02-connectors.md):
  <!-- FILL: e.g. `make refresh-data` → re-fetches, validates, replaces fixtures -->

## RPO / RTO

<!-- FILL: how much data loss is acceptable (RPO) and how fast restore must be (RTO);
pick the backup schedule from that. -->
