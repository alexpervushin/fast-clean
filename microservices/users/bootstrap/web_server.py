from contextlib import asynccontextmanager

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from microservices.shared.infrastructure.database.orm import BaseModel
from microservices.shared.infrastructure.database.session import create_engine
from microservices.shared.infrastructure.http.exceptions_handler import (
    register_exception_handlers,
)
from microservices.shared.infrastructure.observability.sentry import setup_sentry
from microservices.users.infrastructure.config import Settings, get_settings
from microservices.users.infrastructure.di.providers import container
from microservices.users.presentation.rest.controllers import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    settings = await container.get(Settings)

    engine = create_engine(settings)

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    yield

    await container.close()


def create_app() -> FastAPI:
    settings = get_settings()

    setup_sentry(settings)

    app = FastAPI(lifespan=lifespan)

    setup_dishka(container, app)

    register_exception_handlers(app)

    routers = (users_router,)

    for router in routers:
        app.include_router(router)

    return app


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "microservices.users.bootstrap.web_server:create_app",
        workers=settings.server.workers,
        host="0.0.0.0",
        port=settings.server.port,
        root_path=settings.server.root_path,
    )
