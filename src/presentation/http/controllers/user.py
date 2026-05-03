from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends
from fastapi_error_map import ErrorAwareRouter
from pydantic import ValidationError
from starlette import status

from application.exceptions import (
    CurrentUserDontAssignError,
    CurrentUserNotFound,
    GatewayFailedError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from domain.exceptions import DomainError, DomainFieldError
from presentation.exceptions import log_info
from presentation.handlers import (
    ChangeUserPasswordHandler,
    GetUserHandler,
    RegisterUserHandler,
    UpdateUserActivationKeyHandler,
)
from presentation.models import (
    UserAuth,
    UserActivationKeyUpdated,
    UserPasswordChange,
    UserRead,
    UserRegister,
    UserRegistered,
)

from .dependencies import authorize, service_unavailable_rule


def create_user_router() -> APIRouter:
    router = ErrorAwareRouter(prefix="/users", tags=["users"])

    @router.post(
        "/",
        error_map={
            ValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            DomainFieldError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            UserAlreadyExistsError: status.HTTP_409_CONFLICT,
            GatewayFailedError: service_unavailable_rule,
        },
        default_on_error=log_info,
        status_code=status.HTTP_201_CREATED,
        response_model=UserRegistered,
    )
    @inject
    async def register(
        request_body: UserRegister,
        handler: FromDishka[RegisterUserHandler],
    ):
        return await handler.execute(request_body)

    @router.get(
        "/profile",
        error_map={
            ValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            DomainFieldError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            UserNotFoundError: status.HTTP_404_NOT_FOUND,
            GatewayFailedError: service_unavailable_rule,
        },
        default_on_error=log_info,
        status_code=status.HTTP_200_OK,
        response_model=UserRead,
    )
    @inject
    async def profile(
        auth_info: Annotated[UserAuth, Depends(authorize)],
        handler: FromDishka[GetUserHandler],
    ):
        return await handler.execute(user_id=auth_info.id)

    @router.patch(
        "/password",
        dependencies=[Depends(authorize)],
        error_map={
            ValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            DomainFieldError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            DomainError: status.HTTP_409_CONFLICT,
            CurrentUserDontAssignError: status.HTTP_401_UNAUTHORIZED,
            CurrentUserNotFound: status.HTTP_401_UNAUTHORIZED,
            GatewayFailedError: service_unavailable_rule,
        },
        default_on_error=log_info,
        status_code=status.HTTP_204_NO_CONTENT,
    )
    @inject
    async def change_password(
        request_body: UserPasswordChange,
        handler: FromDishka[ChangeUserPasswordHandler],
    ):
        await handler.execute(request_body)

    @router.patch(
        "/activation-key",
        dependencies=[Depends(authorize)],
        error_map={
            ValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            CurrentUserDontAssignError: status.HTTP_401_UNAUTHORIZED,
            CurrentUserNotFound: status.HTTP_401_UNAUTHORIZED,
            GatewayFailedError: service_unavailable_rule,
        },
        default_on_error=log_info,
        status_code=status.HTTP_200_OK,
        response_model=UserActivationKeyUpdated,
    )
    @inject
    async def update_activation_key(
        handler: FromDishka[UpdateUserActivationKeyHandler],
    ):
        return await handler.execute()

    return router
