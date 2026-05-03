import logging

from application.events import UserActivationKeyGenerated
from application.ports.notifiers import UserActivationKeyGeneratedNotifier
from infrastructure.adapters.task_queue import NotificationTaskQueue


logger = logging.getLogger(__name__)


class CeleryUserActivationKeyGeneratedNotifier(UserActivationKeyGeneratedNotifier):
    def __init__(
        self,
        task_queue: NotificationTaskQueue,
    ):
        self._task_queue = task_queue

    async def notify(self, message: UserActivationKeyGenerated) -> bool:
        logger.info("Ставим задачу отправки ключа активации для %s", message.user_email)
        self._task_queue.send_activation_key_email(
            user_email=message.user_email,
            activation_key=message.activation_key,
        )
        return True
