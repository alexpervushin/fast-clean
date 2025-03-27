from contextlib import asynccontextmanager

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from services.shared.infrastructure.database import create_engine
from services.shared.infrastructure.exceptions_handler import (
    register_exception_handlers,
)
from services.shared.infrastructure.orm.base_models import BaseModel
from services.shared.infrastructure.sentry import setup_sentry
from services.users.infrastructure.di.container import container
from services.users.infrastructure.settings import Settings, get_settings
from services.users.presentation.rest.http import router as users_router


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
        "services.users.infrastructure.bootstrap.rest:create_app",
        workers=settings.server.workers,
        host="0.0.0.0",  # noqa: S104
        port=settings.server.port,
        root_path=settings.server.root_path,
    )
