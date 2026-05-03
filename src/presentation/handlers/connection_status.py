import logging
from uuid import UUID

from application.ports import ConnectionStatusSubscriber
from domain.entities.user import UserId
from presentation.exceptions import InvalidAccessTokenError
from presentation.models import WebSocketErrorCode
from presentation.presenters import JwtAuthPresenter
from presentation.ws import ConnectionStatusConnection, WebSocketCloseCode


logger = logging.getLogger(__name__)


class ConnectionStatusHandler:
    def __init__(
        self,
        auth_presenter: JwtAuthPresenter,
        subscriber: ConnectionStatusSubscriber,
    ):
        self._auth_presenter = auth_presenter
        self._subscriber = subscriber

    async def execute(
        self,
        token: str,
        connection: ConnectionStatusConnection,
        expected_user_id: UUID | None = None,
    ) -> None:
        await connection.accept()

        try:
            auth_info = self._auth_presenter.decode(token)
        except InvalidAccessTokenError:
            await connection.send_error(
                WebSocketErrorCode.UNAUTHORIZED,
                "Некорректный токен доступа",
            )
            await connection.close(WebSocketCloseCode.UNAUTHORIZED)
            return

        if expected_user_id is not None and auth_info.id != expected_user_id:
            await connection.send_error(
                WebSocketErrorCode.FORBIDDEN,
                "Идентификатор пользователя не совпадает с токеном",
            )
            await connection.close(WebSocketCloseCode.FORBIDDEN)
            return

        user_id = UserId(auth_info.id)
        logger.info("WebSocket подключен user_id=%s", user_id.value)
        try:
            async for event in self._subscriber.listen(user_id):
                await connection.send_status(event)
        finally:
            logger.info("WebSocket отключен user_id=%s", user_id.value)
