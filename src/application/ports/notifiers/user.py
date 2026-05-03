from application.events import UserActivationKeyGenerated


class UserActivationKeyGeneratedNotifier:
    async def notify(self, event: UserActivationKeyGenerated) -> bool:
        return True
