"""FastAPI factory. Takes an assembled ItemService so tests inject the in-memory
twin; the deployable app is wired in app.composition (the only wiring root)."""

from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.application.item_service import ItemService
from app.domain.models import ValidationError
from app.infrastructure.api.routes import build_router

log = logging.getLogger(__name__)


def create_app(service: ItemService) -> FastAPI:
    app = FastAPI(title="PROJECT_NAME backend")
    app.include_router(build_router(service))

    @app.exception_handler(ValidationError)
    async def on_validation_error(request: Request, exc: ValidationError) -> JSONResponse:
        log.error("validation error on %s: %s", request.url.path, exc)
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
