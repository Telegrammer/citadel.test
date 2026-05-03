from .base import DomainError


class InvalidNewPasswordError(DomainError): ...


class InvalidActvationKeyError(DomainError): ...


class ActivationKeyIsExpiredError(DomainError): ...
