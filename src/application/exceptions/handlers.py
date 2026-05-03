import functools
import logging
from collections.abc import Awaitable, Callable

from .base import ApplicationError, GatewayFailedError


logger = logging.getLogger(__name__)


def retry_on_conflict[
    conflictT: ApplicationError,
](
    error: type[conflictT],
    max_retries: int = 3,
):
    def decorator[**P, T](
        command: Callable[P, Awaitable[T]],
    ) -> Callable[P, Awaitable[T]]:
        @functools.wraps(command)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            last_error: conflictT | None = None

            for attempt in range(1, max_retries + 1):
                try:
                    return await command(*args, **kwargs)
                except error as exc:
                    last_error = exc

                    if attempt == max_retries:
                        logger.info("Повторные попытки после конфликта исчерпаны")
                        raise

                    logger.info("Обнаружен конфликт, выполняется повторная попытка")

            if last_error is not None:
                raise last_error

            raise GatewayFailedError(
                "retry_failed",
                "Цикл повторных попыток завершился неожиданно",
            )

        return wrapper

    return decorator
