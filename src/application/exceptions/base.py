class ApplicationError(Exception):
    def __init__(self, code: str, message: str = ""):
        super().__init__(message)
        self.code = code


class UsecaseError(ApplicationError): ...


class GatewayFailedError(ApplicationError): ...


class AccessDeniedError(ApplicationError): ...


class CurrentUserDontAssignError(ApplicationError): ...
