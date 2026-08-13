"""HTTP routes for items. Schemas are inlined here — they are the HTTP contract,
mirrored 1:1 by frontend/src/api/types.ts (change both in the same task)."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from app.application.item_service import ItemService


class ItemIn(BaseModel):
    name: str
    source: str


class ItemOut(BaseModel):
    id: int
    name: str
    source: str
    created_at: datetime


def build_router(service: ItemService) -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.get("/items", response_model=list[ItemOut])
    def list_items() -> list[ItemOut]:
        return [ItemOut(id=i.id, name=i.name, source=i.source, created_at=i.created_at) for i in service.list_items()]  # type: ignore[arg-type]

    @router.post("/items", response_model=ItemOut, status_code=201)
    def create_item(payload: ItemIn) -> ItemOut:
        item = service.create_item(payload.name, payload.source)
        return ItemOut(id=item.id, name=item.name, source=item.source, created_at=item.created_at)  # type: ignore[arg-type]

    return router
