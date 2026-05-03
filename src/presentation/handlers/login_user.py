from application.compositions import LoginUserComposition
from application.usecase.login_user import LoginUserRequest, LoginUserResponse
from presentation.models import UserEntered, UserLogin
from presentation.presenters import JwtAuthPresenter


class LoginUserHandler:
    def __init__(
        self,
        composition: LoginUserComposition,
        auth_presenter: JwtAuthPresenter,
    ):
        self._composition = composition
        self._auth_presenter = auth_presenter

    async def execute(self, request: UserLogin) -> UserEntered:
        response: LoginUserResponse = await self._composition(
            LoginUserRequest.from_primitives(
                email=request.email,
                password=request.password,
            )
        )

        return UserEntered(
            access_token=self._auth_presenter.encode(response),
            token_type="Bearer",
        )
