from application.compositions import RegisterUserComposition
from application.usecase.register_user import RegisterUserRequest, RegisterUserResponse
from presentation.models import UserRegister, UserRegistered


class RegisterUserHandler:
    def __init__(self, composition: RegisterUserComposition):
        self._composition = composition

    async def execute(self, request: UserRegister) -> UserRegistered:
        response: RegisterUserResponse = await self._composition(
            RegisterUserRequest.from_primitives(
                email=request.email,
                password=request.password,
            )
        )

        return UserRegistered(
            id=response.id.value,
        )
