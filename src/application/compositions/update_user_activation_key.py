import logging

from application.events import UserActivationKeyGenerated
from application.ports import UnitOfWork
from application.ports.notifiers import UserActivationKeyGeneratedNotifier
from application.usecase.update_user_activation_key import (
    UpdateUserActivationKeyResponse,
    UpdateUserActivationKeyUsecase,
)


logger = logging.getLogger(__name__)


class UpdateUserActivationKeyComposition:
    def __init__(
        self,
        usecase: UpdateUserActivationKeyUsecase,
        unit_of_work: UnitOfWork,
        notifier: UserActivationKeyGeneratedNotifier,
    ):
        self._usecase = usecase
        self._unit_of_work = unit_of_work
        self._notifier = notifier

    async def __call__(self) -> str:

        logger.info("Начато обновление ключа активации пользователя")

        async with self._unit_of_work:
            response: UpdateUserActivationKeyResponse = await self._usecase()

        await self._notifier.notify(
            UserActivationKeyGenerated(
                user_email=response.email,
                activation_key=response.activation_key,
            )
        )
        logger.info("Ключ активации пользователя обновлен")

        return response.email
