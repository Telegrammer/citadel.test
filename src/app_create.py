from collections.abc import Mapping, Sequence
from contextlib import asynccontextmanager
import logging
import sys

import dishka.integrations.fastapi as fastapi_integration
from dishka import AsyncContainer, Provider, make_async_container
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from presentation.http.controllers import app_router
from setup.config import Settings, settings
from setup.db_helper import DatabaseHelper
from setup.providers import (
    ApplicationProvider,
    DatabaseProvider,
    DomainProvider,
    NotificationProvider,
    PresentationProvider,
    RedisProvider,
)
from setup.redis_helper import RedisHelper


logger = logging.getLogger(__name__)


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)


def create_container(
    app_settings: Settings = settings,
    extra_context: Mapping[type[object], object] | None = None,
    extra_providers: Sequence[Provider] = (),
) -> AsyncContainer:
    context: dict[type[object], object] = {Settings: app_settings}

    if extra_context:
        context.update(extra_context)

    return make_async_container(
        DatabaseProvider(),
        RedisProvider(),
        NotificationProvider(),
        DomainProvider(),
        ApplicationProvider(),
        PresentationProvider(),
        *extra_providers,
        context=context,
    )


def create_app(
    app_settings: Settings = settings,
    extra_context: Mapping[type[object], object] | None = None,
    extra_providers: Sequence[Provider] = (),
) -> FastAPI:
    configure_logging()
    logger.info("Логирование приложения настроено")

    container = create_container(
        app_settings=app_settings,
        extra_context=extra_context,
        extra_providers=extra_providers,
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        redis_helper = await container.get(RedisHelper)
        await redis_helper.broker.start()

        yield

        await redis_helper.close()
        db_helper = await container.get(DatabaseHelper)
        await db_helper.dispose()
        await container.close()

    app = FastAPI(lifespan=lifespan)
    app.include_router(app_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    fastapi_integration.setup_dishka(container=container, app=app)
    return app
