"""Item repository adapters: SQL and in-memory twins.

The twin pattern is the offline-mode seam — tests and offline runs use InMemory,
the composed app uses Sql. Both satisfy app.domain.ports.ItemRepository.
"""

from __future__ import annotations

import itertools

from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, insert, select
from sqlalchemy.engine import Engine

from app.domain.models import Item

metadata = MetaData()

items_table = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("source", String, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
)


class SqlItemRepository:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def add(self, item: Item) -> Item:
        with self._engine.begin() as conn:
            item_id = conn.execute(
                insert(items_table)
                .values(name=item.name, source=item.source, created_at=item.created_at)
                .returning(items_table.c.id)
            ).scalar_one()
        return Item(id=item_id, name=item.name, source=item.source, created_at=item.created_at)

    def list_all(self) -> list[Item]:
        with self._engine.connect() as conn:
            rows = conn.execute(select(items_table).order_by(items_table.c.id)).all()
        return [Item(id=r.id, name=r.name, source=r.source, created_at=r.created_at) for r in rows]


class InMemoryItemRepository:
    def __init__(self) -> None:
        self._items: list[Item] = []
        self._ids = itertools.count(1)

    def add(self, item: Item) -> Item:
        stored = Item(id=next(self._ids), name=item.name, source=item.source, created_at=item.created_at)
        self._items.append(stored)
        return stored

    def list_all(self) -> list[Item]:
        return list(self._items)
