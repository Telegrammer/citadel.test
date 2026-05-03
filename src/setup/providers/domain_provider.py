from datetime import timedelta

from dishka import Provider, Scope, from_context, provide

from domain.entities.user import UserId
from domain.entities.virtual_machine import VirtualMachineId
from domain.ports import ActivationKeyGenerator, Hasher, IdGenerator
from domain.services import UserService, VirtualMachineService
from infrastructure.adapters.activation_key_generator import SecretsActivationKeyGenerator
from infrastructure.adapters.hasher import BcryptHasher
from infrastructure.adapters.id_generator import (
    Uuid4UserIdGenerator,
    Uuid4VirtualMachineIdGenerator,
)
from setup.config import Settings


class DomainProvider(Provider):
    scope = Scope.APP

    settings = from_context(Settings)

    hasher = provide(source=BcryptHasher, provides=Hasher)
    user_id_generator = provide(
        source=Uuid4UserIdGenerator,
        provides=IdGenerator[UserId],
    )
    virtual_machine_id_generator = provide(
        source=Uuid4VirtualMachineIdGenerator,
        provides=IdGenerator[VirtualMachineId],
    )
    @provide
    def provide_activation_key_generator(self, hasher: Hasher) -> ActivationKeyGenerator:
        return SecretsActivationKeyGenerator(hasher=hasher)

    @provide
    def provide_user_service(
        self,
        settings: Settings,
        id_generator: IdGenerator[UserId],
        hasher: Hasher,
        activation_key_generator: ActivationKeyGenerator,
    ) -> UserService:
        return UserService(
            id_generator=id_generator,
            hasher=hasher,
            activation_key_generator=activation_key_generator,
            activation_key_expiration_duration=timedelta(
                minutes=settings.service.activation_key_expiration_minutes
            ),
        )

    @provide
    def provide_virtual_machine_service(
        self,
        id_generator: IdGenerator[VirtualMachineId],
    ) -> VirtualMachineService:
        return VirtualMachineService(id_generator=id_generator)
