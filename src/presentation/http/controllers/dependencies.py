from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi_error_map import rule
from dishka.integrations.fastapi import FromDishka, inject
from starlette import status

from application.ports.gateways import UserQueryGateway
from application.services import CurrentUserService
from domain.entities.user import UserId
from presentation.exceptions import InvalidAccessTokenError, log_error
from presentation.exceptions.translators import ServiceUnavailableTranslator
from presentation.models import UserAuth, VirtualMachineClaim
from presentation.presenters import JwtAuthPresenter


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

service_unavailable_rule = rule(
    status=status.HTTP_503_SERVICE_UNAVAILABLE,
    translator=ServiceUnavailableTranslator(),
    on_error=log_error,
)


@inject
async def authorize(
    auth_presenter: FromDishka[JwtAuthPresenter],
    current_user_service: FromDishka[CurrentUserService],
    token: str = Depends(oauth2_scheme),
) -> UserAuth:
    try:
        auth_info: UserAuth = auth_presenter.decode(token)
    except InvalidAccessTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректные учетные данные",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    current_user_service.set_user(UserId(auth_info.id))
    return auth_info


@inject
async def authorize_by_activation_key(
    request_body: VirtualMachineClaim,
    user_queries: FromDishka[UserQueryGateway],
    current_user_service: FromDishka[CurrentUserService],
) -> None:
    try:
        lookup, _ = request_body.activation_key.split(".", maxsplit=1)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный ключ активации",
        ) from exc

    user = await user_queries.by_activation_key_lookup(lookup)

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный ключ активации",
        )

    current_user_service.set_user(user.id)
