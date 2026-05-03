import logging

from application.usecase.login_user import (
    LoginUserRequest,
    LoginUserResponse,
    LoginUserUsecase,
)


logger = logging.getLogger(__name__)


class LoginUserComposition:
    def __init__(self, usecase: LoginUserUsecase):
        self._usecase = usecase

    async def __call__(self, request: LoginUserRequest) -> LoginUserResponse:

        logger.info("Login process started")
        response: LoginUserResponse = await self._usecase(request)
        logger.info("User %s successfully logged in at %s", response.id, response.login_at)

        return response
