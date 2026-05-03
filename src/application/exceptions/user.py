from .base import UsecaseError


class UserAlreadyExistsError(UsecaseError): ...


class UserNotFoundError(UsecaseError): ...


class CurrentUserNotFound(UsecaseError): ...
