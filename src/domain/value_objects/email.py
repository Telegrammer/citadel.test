import re
from dataclasses import dataclass

from domain.exceptions import DomainFieldError


@dataclass(init=False)
class EmailAddress:
    __pattern: re.Pattern = re.compile(
        r"""^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"""
    )

    def __init__(self, value: str):
        if not EmailAddress.__pattern.fullmatch(value):
            raise DomainFieldError(
                code="invalid_email",
                field="email",
                message=f"Given value {value} is not a valid email address",
            )
        self.value = value
