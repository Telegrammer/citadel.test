import logging

from application.events import UserActivationKeyGenerated
from infrastructure.adapters.smtp_client import SMTPClient
from setup.celery_app import celery_app
from setup.config import settings


logger = logging.getLogger(__name__)


@celery_app.task(name="notifications.send_activation_key_email")
def send_activation_key_email(user_email: str, activation_key: str) -> None:
    logger.info(
        "Отправляем письмо с ключом активации для %s через %s:%s",
        user_email,
        settings.smtp.host,
        settings.smtp.port,
    )
    message = UserActivationKeyGenerated(
        user_email=user_email,
        activation_key=activation_key,
    )
    smtp_client = SMTPClient(
        host=settings.smtp.host,
        port=settings.smtp.port,
        sender_email=settings.smtp.sender_email,
        username=settings.smtp.username,
        password=settings.smtp.password,
        use_tls=settings.smtp.use_tls,
        timeout=settings.smtp.timeout,
    )
    smtp_client.send_sync(
        recipient=message.user_email,
        subject="Ключ активации виртуальной машины",
        body=(
            "Здравствуйте.\n\n"
            "Ваш ключ активации виртуальной машины:\n"
            f"{message.activation_key}\n\n"
            "Если вы не запрашивали ключ, проигнорируйте это сообщение."
        ),
    )
    logger.info("Письмо с ключом активации отправлено для %s", user_email)
