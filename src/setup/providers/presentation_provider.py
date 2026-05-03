from dishka import Provider, Scope, from_context, provide

from presentation.handlers import (
    AddVirtualMachineHandler,
    ChangeUserPasswordHandler,
    ClaimVirtualMachineHandler,
    ConnectionStatusHandler,
    FreeVirtualMachineHandler,
    GetUserHandler,
    LoginUserHandler,
    RegisterUserHandler,
    UpdateUserActivationKeyHandler,
)
from presentation.presenters import JwtAuthPresenter
from setup.config import Settings


class PresentationProvider(Provider):
    scope = Scope.REQUEST

    settings = from_context(Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def provide_auth_presenter(self, settings: Settings) -> JwtAuthPresenter:
        return JwtAuthPresenter(
            secret_key=settings.auth.secret_key.read_text(),
            public_key=settings.auth.public_key.read_text(),
            algorithm=settings.auth.algorithm,
        )

    register_user_handler = provide(RegisterUserHandler)
    login_user_handler = provide(LoginUserHandler)
    get_user_handler = provide(GetUserHandler)
    change_password_handler = provide(ChangeUserPasswordHandler)
    update_user_activation_key_handler = provide(UpdateUserActivationKeyHandler)
    add_virtual_machine_handler = provide(AddVirtualMachineHandler)
    claim_virtual_machine_handler = provide(ClaimVirtualMachineHandler)
    free_virtual_machine_handler = provide(FreeVirtualMachineHandler)
    connection_status_handler = provide(ConnectionStatusHandler, scope=Scope.SESSION)
