"""Domain models: frozen dataclasses, no framework imports (lint-enforced)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


class ValidationError(ValueError):
    """Raised by use cases on invalid input; the API maps it to HTTP 422."""


@dataclass(frozen=True)
class Item:
    """Every datum carries a `source`: file:<path> | api:<name> | url:<addr> | manual:<who>."""

    id: int | None
    name: str
    source: str
    created_at: datetime


@dataclass(frozen=True)
class Job:
    """Lease-queue job. Lifecycle: queued -> leased -> done | failed (or re-queued)."""

    id: int | None
    kind: str
    payload: str
    status: str
    attempts: int
    lease_until: datetime | None
