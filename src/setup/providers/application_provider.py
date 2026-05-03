from datetime import timedelta

from dishka import Provider, Scope, from_context, provide

from application.compositions import (
    AddVirtualMachineComposition,
    ChangeUserPasswordComposition,
    ClaimVirtualMachineComposition,
    FreeVirtualMachineComposition,
    GetUserComposition,
    LoginUserComposition,
    RegisterUserComposition,
    UpdateUserActivationKeyComposition,
)
from application.ports import Clock
from application.ports.gateways import (
    UserCommandGateway,
    UserQueryGateway,
    VirtualMachineCommandGateway,
    VirtualMachineQueryGateway,
)
from application.services import CurrentUserService
from application.usecase.add_virtual_machine import AddVirtualMachineUsecase
from application.usecase.change_password import LoginUserUsecase as ChangePasswordUsecase
from application.usecase.claim_virtual_machine import ClaimVirtualMachineUsecase
from application.usecase.free_virtual_machine import FreeVirtualMachineUsecase
from application.usecase.get_user import GetUserUsecase
from application.usecase.login_user import LoginUserUsecase
from application.usecase.register_user import RegisterUserUsecase
from application.usecase.update_user_activation_key import (
    UpdateUserActivationKeyUsecase,
)
from domain.ports import Hasher
from infrastructure.adapters.clock import TimestampClock
from infrastructure.adapters.gateways import (
    SQLAlchemyUserCommandGateway,
    SQLAlchemyUserQueryGateway,
    SQLAlchemyVirtualMachineCommandGateway,
    SQLAlchemyVirtualMachineQueryGateway,
)
from infrastructure.adapters.mappers import (
    SQLAlchemyUserMapper,
    SQLAlchemyVirtualMachineMapper,
)
from setup.config import Settings


class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    settings = from_context(Settings, scope=Scope.APP)

    clock = provide(source=TimestampClock, provides=Clock, scope=Scope.APP)

    user_mapper = provide(SQLAlchemyUserMapper)
    virtual_machine_mapper = provide(SQLAlchemyVirtualMachineMapper)

    user_commands = provide(
        source=SQLAlchemyUserCommandGateway,
        provides=UserCommandGateway,
    )
    user_queries = provide(
        source=SQLAlchemyUserQueryGateway,
        provides=UserQueryGateway,
    )
    virtual_machine_commands = provide(
        source=SQLAlchemyVirtualMachineCommandGateway,
        provides=VirtualMachineCommandGateway,
    )
    virtual_machine_queries = provide(
        source=SQLAlchemyVirtualMachineQueryGateway,
        provides=VirtualMachineQueryGateway,
    )

    current_user_service = provide(CurrentUserService)

    @provide
    def provide_dummy_hash(self, settings: Settings, hasher: Hasher) -> bytes:
        return hasher.hash(settings.service.dummy_password)

    @provide(scope=Scope.APP)
    def provide_login_duration(self, settings: Settings) -> timedelta:
        return timedelta(minutes=settings.service.login_duration_minutes)

    register_user_usecase = provide(RegisterUserUsecase)
    register_user_composition = provide(RegisterUserComposition)

    login_user_usecase = provide(LoginUserUsecase)
    login_user_composition = provide(LoginUserComposition)

    get_user_usecase = provide(GetUserUsecase)
    get_user_composition = provide(GetUserComposition)

    change_password_usecase = provide(ChangePasswordUsecase)
    change_password_composition = provide(ChangeUserPasswordComposition)

    update_user_activation_key_usecase = provide(UpdateUserActivationKeyUsecase)
    update_user_activation_key_composition = provide(UpdateUserActivationKeyComposition)

    add_virtual_machine_usecase = provide(AddVirtualMachineUsecase)
    add_virtual_machine_composition = provide(AddVirtualMachineComposition)

    claim_virtual_machine_usecase = provide(ClaimVirtualMachineUsecase)
    claim_virtual_machine_composition = provide(ClaimVirtualMachineComposition)

    free_virtual_machine_usecase = provide(FreeVirtualMachineUsecase)
    free_virtual_machine_composition = provide(FreeVirtualMachineComposition)
