"""Wiring root: the ONLY module (with worker.py) that assembles adapters into
services. Everything else depends on ports, never on concrete adapters."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.application.item_service import ItemService
from app.infrastructure.api.app import create_app
from app.infrastructure.persistence.job_queue import PostgresJobQueue
from app.infrastructure.persistence.repositories import SqlItemRepository
from app.settings import Settings, load_settings


def build_engine(settings: Settings) -> Engine:
    return create_engine(settings.database_url, pool_pre_ping=True)


def build_item_service(engine: Engine) -> ItemService:
    return ItemService(SqlItemRepository(engine))


def build_job_queue(settings: Settings, engine: Engine) -> PostgresJobQueue:
    return PostgresJobQueue(engine, settings.job_lease_seconds, settings.job_max_attempts)


def build_api():
    """Uvicorn entrypoint: app.composition:build_api (factory mode)."""
    settings = load_settings()
    return create_app(build_item_service(build_engine(settings)))
