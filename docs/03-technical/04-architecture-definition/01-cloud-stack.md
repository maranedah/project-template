# Cloud stack

Read this when: touching infra, or deciding where a new capability runs.

## Stack (GCP)

| Piece | Choice | Notes |
|---|---|---|
| Compute | Cloud Run v2 (`terraform/backend`, `terraform/frontend`) | scale-to-zero; `cpu_idle=true`, `startup_cpu_boost=true` |
| Storage | GCS (`APP_STORAGE_BACKEND=gcs`) | local FS twin for dev/offline |
| DB | <!-- FILL: Cloud SQL / VM postgres --> | compose `db` locally |
| Network | <!-- FILL: default / VPC connector if private DB --> | |

## Serverless considerations

- Nothing in-process survives scale-to-zero: no background threads, no in-memory
  cron — schedule via Cloud Scheduler hitting an endpoint.
- Cold starts: keep images slim (multi-stage builds), avoid heavy imports at startup.

## Workers for long tasks (>30 s or retryable)

Included but disabled: a Postgres lease queue (`FOR UPDATE SKIP LOCKED`, lease +
max-attempts in `backend/app/infrastructure/persistence/job_queue.py`) and a worker
loop (`backend/app/worker.py`). The API only enqueues (202 + poll); the worker claims.
Enable by uncommenting the `worker` service in `docker-compose.yml`.

Deploy variants seen in prior projects: same image as a second Cloud Run service
(CPU-light jobs) · GCE Spot VMs started/stopped around the queue (heavy/scraping) ·
dedicated image with its own Dockerfile when deps are heavy (GPU/ML — split the
image, cache model files in a volume).
