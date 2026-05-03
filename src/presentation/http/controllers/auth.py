from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_error_map import ErrorAwareRouter
from pydantic import ValidationError
from starlette import status

from application.exceptions import GatewayFailedError, UserNotFoundError
from domain.exceptions import DomainFieldError
from presentation.exceptions import log_info
from presentation.handlers import LoginUserHandler
from presentation.models import UserEntered, UserLogin

from .dependencies import service_unavailable_rule


def create_auth_router() -> APIRouter:
    router = ErrorAwareRouter(prefix="/auth", tags=["auth"])

    @router.post(
        "/login",
        error_map={
            ValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            DomainFieldError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            UserNotFoundError: status.HTTP_401_UNAUTHORIZED,
            GatewayFailedError: service_unavailable_rule,
        },
        default_on_error=log_info,
        status_code=status.HTTP_200_OK,
        response_model=UserEntered,
    )
    @inject
    async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        handler: FromDishka[LoginUserHandler],
    ):
        return await handler.execute(
            UserLogin(
                email=form_data.username,
                password=form_data.password,
            )
        )

    return router
