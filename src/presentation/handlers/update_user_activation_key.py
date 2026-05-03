from application.compositions import UpdateUserActivationKeyComposition
from presentation.models import UserActivationKeyUpdated


class UpdateUserActivationKeyHandler:
    def __init__(self, composition: UpdateUserActivationKeyComposition):
        self._composition = composition

    async def execute(self) -> UserActivationKeyUpdated:
        email: str = await self._composition()

        return UserActivationKeyUpdated(email=email)
