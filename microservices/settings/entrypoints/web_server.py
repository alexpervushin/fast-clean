from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from microservices.shared.infrastructure.database.orm import BaseModel
from microservices.shared.infrastructure.database.session import create_engine
from microservices.shared.infrastructure.http.exceptions_handler import (
    register_exception_handlers,
)
from microservices.shared.infrastructure.observability.sentry import setup_sentry
from microservices.settings.infrastructure.config import Settings, get_settings
from microservices.settings.infrastructure.di.providers import container
from microservices.settings.presentation.rest.settings_controllers import router as settings_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    lifespan_settings = await container.get(Settings)

    engine = create_engine(lifespan_settings)

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    yield

    await container.close()


def create_app() -> FastAPI:
    app_settings = get_settings()

    if app_settings.sentry and app_settings.sentry.dsn:
        setup_sentry(app_settings)


    app = FastAPI(lifespan=lifespan)

    setup_dishka(container, app)

    register_exception_handlers(app)

    app.include_router(settings_router)

    return app


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "microservices.settings.entrypoints.web_server:create_app",
        factory=True,
        workers=settings.server.workers,
        host="0.0.0.0",
        port=settings.server.port,
        root_path=settings.server.root_path or "",
    )