"""Postgres lease queue: FOR UPDATE SKIP LOCKED claim, lease timeout, max attempts.

Broker-less worker pattern: the API enqueues, workers claim atomically — a racing
worker's claim matches zero rows and moves on. Expired leases (crashed worker) are
reclaimed automatically. Postgres-only SQL; the InMemory twin backs tests.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import text
from sqlalchemy.engine import Engine

from app.domain.models import Job

_CLAIM_SQL = text(
    """
    SELECT id FROM jobs
    WHERE status = 'queued' OR (status = 'leased' AND lease_until < now())
    ORDER BY id
    FOR UPDATE SKIP LOCKED
    LIMIT 1
    """
)


class PostgresJobQueue:
    def __init__(self, engine: Engine, lease_seconds: int, max_attempts: int) -> None:
        self._engine = engine
        self._lease_seconds = lease_seconds
        self._max_attempts = max_attempts

    def enqueue(self, kind: str, payload: str) -> Job:
        with self._engine.begin() as conn:
            job_id = conn.execute(
                text(
                    "INSERT INTO jobs (kind, payload, status, attempts)"
                    " VALUES (:kind, :payload, 'queued', 0) RETURNING id"
                ),
                {"kind": kind, "payload": payload},
            ).scalar_one()
        return Job(id=job_id, kind=kind, payload=payload, status="queued", attempts=0, lease_until=None)

    def claim(self) -> Job | None:
        with self._engine.begin() as conn:
            row = conn.execute(_CLAIM_SQL).first()
            if row is None:
                return None
            claimed = conn.execute(
                text(
                    "UPDATE jobs SET status = 'leased', attempts = attempts + 1,"
                    " lease_until = now() + make_interval(secs => :lease)"
                    " WHERE id = :id RETURNING id, kind, payload, status, attempts, lease_until"
                ),
                {"id": row.id, "lease": self._lease_seconds},
            ).one()
        return Job(
            id=claimed.id,
            kind=claimed.kind,
            payload=claimed.payload,
            status=claimed.status,
            attempts=claimed.attempts,
            lease_until=claimed.lease_until,
        )

    def complete(self, job_id: int) -> None:
        with self._engine.begin() as conn:
            conn.execute(
                text("UPDATE jobs SET status = 'done', lease_until = NULL WHERE id = :id"),
                {"id": job_id},
            )

    def fail(self, job_id: int) -> None:
        """Re-queue for retry, or mark failed once max attempts is reached."""
        with self._engine.begin() as conn:
            conn.execute(
                text(
                    "UPDATE jobs SET"
                    " status = CASE WHEN attempts >= :max THEN 'failed' ELSE 'queued' END,"
                    " lease_until = NULL"
                    " WHERE id = :id"
                ),
                {"id": job_id, "max": self._max_attempts},
            )


class InMemoryJobQueue:
    """Test/offline twin. Single-process only — no real locking needed."""

    def __init__(self, lease_seconds: int = 300, max_attempts: int = 3) -> None:
        self._jobs: dict[int, Job] = {}
        self._next_id = 1
        self._lease_seconds = lease_seconds
        self._max_attempts = max_attempts

    def enqueue(self, kind: str, payload: str) -> Job:
        job = Job(id=self._next_id, kind=kind, payload=payload, status="queued", attempts=0, lease_until=None)
        self._jobs[self._next_id] = job
        self._next_id += 1
        return job

    def claim(self) -> Job | None:
        now = datetime.now(UTC)
        for job in sorted(self._jobs.values(), key=lambda j: j.id or 0):
            expired = job.status == "leased" and job.lease_until is not None and job.lease_until < now
            if job.status == "queued" or expired:
                claimed = Job(
                    id=job.id,
                    kind=job.kind,
                    payload=job.payload,
                    status="leased",
                    attempts=job.attempts + 1,
                    lease_until=now + timedelta(seconds=self._lease_seconds),
                )
                self._jobs[job.id] = claimed  # type: ignore[index]
                return claimed
        return None

    def complete(self, job_id: int) -> None:
        job = self._jobs[job_id]
        self._jobs[job_id] = Job(
            id=job.id, kind=job.kind, payload=job.payload, status="done", attempts=job.attempts, lease_until=None
        )

    def fail(self, job_id: int) -> None:
        job = self._jobs[job_id]
        status = "failed" if job.attempts >= self._max_attempts else "queued"
        self._jobs[job_id] = Job(
            id=job.id, kind=job.kind, payload=job.payload, status=status, attempts=job.attempts, lease_until=None
        )
