"""Item use cases. Application layer: depends on domain only (lint-enforced)."""

from __future__ import annotations

from datetime import UTC, datetime

from app.domain.models import Item, ValidationError
from app.domain.ports import ItemRepository


class ItemService:
    def __init__(self, repo: ItemRepository) -> None:
        self._repo = repo

    def create_item(self, name: str, source: str) -> Item:
        name = name.strip()
        source = source.strip()
        if not name:
            raise ValidationError("name must be non-empty")
        if not source:
            raise ValidationError("source must be non-empty (file:|api:|url:|manual:)")
        return self._repo.add(Item(id=None, name=name, source=source, created_at=datetime.now(UTC)))

    def list_items(self) -> list[Item]:
        return self._repo.list_all()
