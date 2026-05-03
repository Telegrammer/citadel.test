from typing import Any
from datetime import datetime, timedelta
from uuid import UUID

import jwt

from application.usecase.login_user import LoginUserResponse
from domain.entities.user import UserId
from presentation.exceptions import InvalidAccessTokenError
from presentation.models import UserAuth


class JwtAuthPresenter:
    def __init__(
        self,
        secret_key: str,
        public_key: str,
        algorithm: str,
    ):
        self._secret_key = secret_key
        self._public_key = public_key
        self._algorithm = algorithm

    def encode(self, payload: LoginUserResponse) -> str:
        return self.encode_access_token(
            user_id=payload.id,
            issued_at=payload.login_at,
            duration=payload.duration,
        )

    def encode_access_token(
        self,
        user_id: UserId,
        issued_at: datetime,
        duration: timedelta,
    ) -> str:
        return jwt.encode(
            {
                "sub": user_id.value.hex,
                "iat": issued_at,
                "exp": issued_at + duration,
            },
            key=self._secret_key,
            algorithm=self._algorithm,
        )

    def decode(self, token: str) -> UserAuth:
        try:
            payload: dict[str, Any] = jwt.decode(
                token,
                key=self._public_key,
                algorithms=[self._algorithm],
            )
            subject = payload.get("sub")
            if subject is None:
                raise InvalidAccessTokenError("Токен не содержит идентификатор пользователя")

            return UserAuth(id=UUID(hex=subject, version=4))
        except (ValueError, jwt.PyJWTError) as exc:
            raise InvalidAccessTokenError("Некорректный токен доступа") from exc
