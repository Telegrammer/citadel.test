import functools
from collections.abc import Awaitable, Callable

from sqlalchemy.exc import DBAPIError, IntegrityError, InterfaceError, OperationalError
from sqlalchemy.orm.exc import StaleDataError

from application.exceptions import ApplicationError, GatewayFailedError


def stale_data_aware(error: Callable[[], ApplicationError]):
    def decorator[**P, T](
        command: Callable[P, Awaitable[T]],
    ) -> Callable[P, Awaitable[T]]:
        @functools.wraps(command)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return await command(*args, **kwargs)
            except StaleDataError as exc:
                raise error() from exc

        return wrapper

    return decorator


def unique_violation_aware(
    constraints: dict[str, tuple[str, str]],
    error: Callable[[str, str], ApplicationError],
):
    def decorator[**P, T](
        command: Callable[P, Awaitable[T]],
    ) -> Callable[P, Awaitable[T]]:
        @functools.wraps(command)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return await command(*args, **kwargs)
            except IntegrityError as exc:
                original_error = exc.orig
                if getattr(original_error, "sqlstate", None) != "23505":
                    raise

                details = repr(original_error)
                for constraint, error_args in constraints.items():
                    if constraint in details:
                        raise error(*error_args) from exc

                raise

        return wrapper

    return decorator


def gateway_failed_aware(message: str):
    def decorator[**P, T](
        command: Callable[P, Awaitable[T]],
    ) -> Callable[P, Awaitable[T]]:
        @functools.wraps(command)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return await command(*args, **kwargs)
            except ApplicationError:
                raise
            except (ConnectionError, DBAPIError, InterfaceError, OperationalError) as exc:
                raise GatewayFailedError("gateway_failed", message) from exc

        return wrapper

    return decorator
