class DomainError(Exception):

    def __init__(self, code: str, message: str = ""):
        super().__init__(message)
        self.code = code


class DomainFieldError(DomainError):

    def __init__(self, code: str, field: str, message: str = ""):
        super().__init__(code, message)
        self.field = field
