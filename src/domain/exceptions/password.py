from enum import StrEnum

from .base import DomainFieldError


class InvalidPasswordReason(StrEnum):
    """Reperesents a list of reasons why password is invalid."""

    TOO_SHORT = "Password is too short"
    NO_DIGITS = "Password must have at least one digit"
    NO_LETERS = "Password must have at least one letter"
    NO_SPECS = "Password must have at least one special character"


class InvalidPasswordError(DomainFieldError):
    """Special domain error for password validation violation."""

    def __init__(self, reason: InvalidPasswordReason):
        super().__init__(
            code="invalid_password",
            field="password",
            message="Given value is not a valid password",
        )
        self.reason = reason
