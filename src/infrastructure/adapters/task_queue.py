from celery import Celery


class NotificationTaskQueue:
    def __init__(self, celery_app: Celery):
        self._celery_app = celery_app

    def send_activation_key_email(
        self,
        user_email: str,
        activation_key: str,
    ) -> None:
        self._celery_app.send_task(
            "notifications.send_activation_key_email",
            kwargs={
                "user_email": user_email,
                "activation_key": activation_key,
            },
        )
