import logging

from application.usecase.get_user import (
    GetUserRequest,
    GetUserResponse,
    GetUserUsecase,
)


logger = logging.getLogger(__name__)


class GetUserComposition:
    def __init__(self, usecase: GetUserUsecase):
        self._usecase = usecase

    async def __call__(self, request: GetUserRequest) -> GetUserResponse:

        logger.info("Fetching user %s", request.user_id)
        response: GetUserResponse = await self._usecase(request)
        logger.info("User %s fetched", request.user_id)

        return response
