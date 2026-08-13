# Observability

Read this when: something failed in prod, or wiring monitoring for a new service.

## Logs

Per-service `logging.yaml`: timestamped lines to stdout, ERROR-and-above duplicated
to `backend/var/log/<service>-errors.log` (`make logs-errors`). Debugging starts there —
one small file, no interleaved noise. In Cloud Run, stdout lands in Cloud Logging;
filter `severity>=ERROR`.

## Minimum alerts (set these up with the first deploy)

| Alert | How |
|---|---|
| Backend down | Cloud Monitoring uptime check on `/health` |
| Stuck jobs (worker enabled) | <!-- FILL: alert on jobs with status=leased and lease_until < now - 10min --> |
| Cost runaway | GCP budget alert (stub in terraform/main.tf) |

## KPIs from logs

<!-- FILL: which KPI-NN numbers are extracted from logs/metrics and how they get
appended to docs/02-planning/tracking/kpis.csv. -->
