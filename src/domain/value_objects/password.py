import re
from dataclasses import dataclass


from domain.exceptions import InvalidPasswordError, InvalidPasswordReason


@dataclass
class PasswordEcncryptionKey:
    value: bytes


@dataclass(init=False)
class Password:
    """Represent a validated password value object.

    This object ensures that the provided password satisfies
    security requirements before being accepted.

    Validation rules:
        - Must meet minimum length requirement.
        - Must contain at least one letter.
        - Must contain at least one digit.
        - Must contain at least one special character.

    Attributes:
        value: Validated password string.

    Raises:
        InvalidPasswordError: If the password does not meet validation rules.
    """

    __min_length: int = 8
    __letters: re.Pattern = re.compile(r".*[a-zA-z]+.*")
    __digits: re.Pattern = re.compile(r".*[0-9]+.*")
    __specials: re.Pattern = re.compile(r".*[^\w].*")

    def __init__(self, value: str):
        if len(value) < Password.__min_length:
            raise InvalidPasswordError(InvalidPasswordReason.TOO_SHORT)
        if not Password.__digits.match(value):
            raise InvalidPasswordError(InvalidPasswordReason.NO_DIGITS)
        if not Password.__letters.match(value):
            raise InvalidPasswordError(InvalidPasswordReason.NO_LETERS)
        if not Password.__specials.match(value):
            raise InvalidPasswordError(InvalidPasswordReason.NO_SPECS)
        self.value = value
