"""Ports: Protocols implemented by infrastructure adapters."""

from __future__ import annotations

from typing import Protocol

from app.domain.models import Item, Job


class ItemRepository(Protocol):
    def add(self, item: Item) -> Item: ...

    def list_all(self) -> list[Item]: ...


class JobQueue(Protocol):
    def enqueue(self, kind: str, payload: str) -> Job: ...

    def claim(self) -> Job | None: ...

    def complete(self, job_id: int) -> None: ...

    def fail(self, job_id: int) -> None: ...
