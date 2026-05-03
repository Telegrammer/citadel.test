import asyncio
import smtplib
from email.message import EmailMessage

from application.exceptions import GatewayFailedError


class SMTPClient:
    def __init__(
        self,
        host: str,
        port: int,
        sender_email: str,
        username: str | None = None,
        password: str | None = None,
        use_tls: bool = True,
        timeout: float = 10.0,
    ):
        self._host = host
        self._port = port
        self._sender_email = sender_email
        self._username = username
        self._password = password
        self._use_tls = use_tls
        self._timeout = timeout

    async def send(
        self,
        recipient: str,
        subject: str,
        body: str,
    ) -> None:
        try:
            await asyncio.to_thread(
                self.send_sync,
                recipient=recipient,
                subject=subject,
                body=body,
            )
        except (OSError, smtplib.SMTPException) as exc:
            raise GatewayFailedError(
                "smtp_failed",
                "Не удалось отправить сообщение через SMTP сервер",
            ) from exc

    def send_sync(
        self,
        recipient: str,
        subject: str,
        body: str,
    ) -> None:
        message = EmailMessage()
        message["From"] = self._sender_email
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        with smtplib.SMTP(
            host=self._host,
            port=self._port,
            timeout=self._timeout,
        ) as smtp:
            if self._use_tls:
                smtp.starttls()

            if self._username and self._password:
                smtp.login(self._username, self._password)

            smtp.send_message(message)
