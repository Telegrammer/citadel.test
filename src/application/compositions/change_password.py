import logging

from application.ports import UnitOfWork
from application.usecase.change_password import (
    ChangeUserPasswordRequest,
    LoginUserUsecase as ChangeUserPasswordUsecase,
)


logger = logging.getLogger(__name__)


class ChangeUserPasswordComposition:
    def __init__(self, usecase: ChangeUserPasswordUsecase, unit_of_work: UnitOfWork):
        self._usecase = usecase
        self._unit_of_work = unit_of_work

    async def __call__(self, request: ChangeUserPasswordRequest) -> None:

        logger.info("Password change started")

        async with self._unit_of_work:
            await self._usecase(request)

        logger.info("Password changed")
