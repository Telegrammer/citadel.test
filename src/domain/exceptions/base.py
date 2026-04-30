class DomainError(Exception):
    """Base exception for domain-level errors.

    Represents an entity integrity and buisness violations
    within the domain layer.

    Attributes:
        code: Short representation of error for search
        message: Human-readable error description.
    """

    def __init__(self, code: str, message: str = ""):
        super().__init__(message)
        self.code = code


class DomainFieldError(DomainError):
    """Domain error associated with a specific field.

    Used when a violation is tied to a particular input field.

    Attributes:
        field: Name of the field that caused the error.
    """

    def __init__(self, code: str, field: str, message: str = ""):
        super().__init__(code, message)
        self.field = field
