"""Alembic environment. URL resolution: APP_DATABASE_SYNC_URL env var, else alembic.ini.

Migrations are handwritten (no autogenerate target metadata needed for apply-only
runs). To autogenerate against the app models, run from backend/.venv:
    APP_DATABASE_SYNC_URL=... .venv/bin/alembic -c db/alembic.ini revision --autogenerate
"""

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def _url() -> str:
    return os.environ.get("APP_DATABASE_SYNC_URL") or config.get_main_option("sqlalchemy.url")


def run_migrations_offline() -> None:
    context.configure(url=_url(), literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_engine(_url())
    with engine.connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
