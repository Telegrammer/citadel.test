import logging
from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from presentation.handlers import ConnectionStatusHandler
from presentation.ws import StarletteConnectionStatusConnection


logger = logging.getLogger(__name__)


def create_connection_status_router() -> APIRouter:
    router = APIRouter(tags=["websocket"])

    @router.websocket("/status/{user_id}")
    @inject
    async def connection_status_by_user(
        websocket: WebSocket,
        user_id: UUID,
        token: Annotated[str, Query(description="JWT access token")],
        handler: FromDishka[ConnectionStatusHandler],
    ) -> None:
        try:
            await handler.execute(
                token=token,
                expected_user_id=user_id,
                connection=StarletteConnectionStatusConnection(websocket),
            )
        except WebSocketDisconnect:
            logger.info("WebSocket клиент отключился user_id=%s", user_id)

    @router.websocket("/status")
    @inject
    async def connection_status(
        websocket: WebSocket,
        token: Annotated[str, Query(description="JWT access token")],
        handler: FromDishka[ConnectionStatusHandler],
    ) -> None:
        try:
            await handler.execute(
                token=token,
                connection=StarletteConnectionStatusConnection(websocket),
            )
        except WebSocketDisconnect:
            logger.info("WebSocket клиент отключился")

    return router
