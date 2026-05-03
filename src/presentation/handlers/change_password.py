from application.compositions import ChangeUserPasswordComposition
from application.usecase.change_password import ChangeUserPasswordRequest
from presentation.models import UserPasswordChange


class ChangeUserPasswordHandler:
    def __init__(self, composition: ChangeUserPasswordComposition):
        self._composition = composition

    async def execute(self, request: UserPasswordChange) -> None:
        await self._composition(
            ChangeUserPasswordRequest.from_primitives(
                current_password=request.current_password,
                new_password=request.new_password,
            )
        )
