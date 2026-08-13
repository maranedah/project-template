"""Lease-queue worker: python -m app.worker

Second composition root. Polls the Postgres lease queue, dispatches by job kind,
finishes the in-flight job on SIGTERM/SIGINT before exiting (a plain kill mid-job
would burn one attempt and wait out the lease).

Disabled by default — enable the `worker` service in docker-compose.yml. When to use:
docs/03-technical/04-architecture-definition/01-cloud-stack.md §workers.
"""

from __future__ import annotations

import logging
import logging.config
import signal
import time
from collections.abc import Callable
from pathlib import Path

import yaml

from app.composition import build_engine, build_job_queue
from app.domain.models import Job
from app.settings import load_settings

log = logging.getLogger(__name__)

_shutdown = False


def _handle_noop(job: Job) -> None:
    """Example handler — replace with real job kinds."""
    log.info("noop job %s payload=%s", job.id, job.payload)


TASK_HANDLERS: dict[str, Callable[[Job], None]] = {
    "noop": _handle_noop,
}


def _setup_logging() -> None:
    config = yaml.safe_load(Path(__file__).resolve().parent.parent.joinpath("logging.yaml").read_text())
    # Same config as the API, but errors go to the worker's own file.
    config["handlers"]["errors"]["filename"] = "var/log/worker-errors.log"
    logging.config.dictConfig(config)


def _request_shutdown(signum: int, frame: object) -> None:
    global _shutdown
    log.info("signal %s received; finishing current job then exiting", signum)
    _shutdown = True


def main() -> None:
    _setup_logging()
    settings = load_settings()
    queue = build_job_queue(settings, build_engine(settings))
    signal.signal(signal.SIGTERM, _request_shutdown)
    signal.signal(signal.SIGINT, _request_shutdown)
    log.info("worker %s started (poll=%ss)", settings.worker_id, settings.worker_poll_interval)

    while not _shutdown:
        job = None
        try:
            job = queue.claim()
            if job is None:
                time.sleep(settings.worker_poll_interval)
                continue
            handler = TASK_HANDLERS.get(job.kind)
            if handler is None:
                log.error("no handler for job kind %r (job %s)", job.kind, job.id)
                queue.fail(job.id)  # type: ignore[arg-type]
                continue
            handler(job)
            queue.complete(job.id)  # type: ignore[arg-type]
        except Exception:
            log.exception("job %s failed", job.id if job else "?")
            if job is not None:
                queue.fail(job.id)  # type: ignore[arg-type]

    log.info("worker stopped")


if __name__ == "__main__":
    main()
