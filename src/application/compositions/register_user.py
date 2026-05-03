import logging

from application.events import UserActivationKeyGenerated
from application.ports import UnitOfWork
from application.usecase.register_user import (
    RegisterUserRequest,
    RegisterUserResponse,
    RegisterUserUsecase,
)
from application.ports.notifiers import UserActivationKeyGeneratedNotifier


logger = logging.getLogger(__name__)


class RegisterUserComposition:
    def __init__(
        self,
        usecase: RegisterUserUsecase,
        unit_of_work: UnitOfWork,
        notifier: UserActivationKeyGeneratedNotifier,
    ):
        self._usecase = usecase
        self._unit_of_work = unit_of_work
        self._notifier = notifier

    async def __call__(self, request: RegisterUserRequest) -> RegisterUserResponse:

        logger.info("User registration started %s", request.email.value)

        async with self._unit_of_work:
            response: RegisterUserResponse = await self._usecase(request)

        await self._notifier.notify(
            UserActivationKeyGenerated(
                user_email=response.email.value,
                activation_key=response.activation_key,
            )
        )
        logger.info("User registered %s", response.id)

        return response
