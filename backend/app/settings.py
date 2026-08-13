"""Runtime settings. Mirrors .env.example — every APP_ var there is a field here."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_")

    env: str = "local"
    log_level: str = "INFO"

    database_url: str = "postgresql+psycopg://app:app@localhost:5532/app"
    database_sync_url: str = "postgresql+psycopg://app:app@localhost:5532/app"

    worker_id: str = "worker-local"
    worker_poll_interval: float = 2.0
    job_lease_seconds: int = 300
    job_max_attempts: int = 3

    storage_backend: str = "local"
    storage_local_root: str = "var/storage"


def load_settings() -> Settings:
    return Settings()
