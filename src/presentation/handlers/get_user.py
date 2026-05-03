from uuid import UUID

from application.compositions import GetUserComposition
from application.usecase.get_user import GetUserRequest, GetUserResponse
from presentation.models import UserRead


class GetUserHandler:
    def __init__(self, composition: GetUserComposition):
        self._composition = composition

    async def execute(self, user_id: UUID) -> UserRead:
        response: GetUserResponse = await self._composition(
            GetUserRequest.from_primitives(user_id=user_id)
        )

        return UserRead(
            email=response.email,
            created_at=response.created_at,
            is_admin=response.is_admin,
        )
