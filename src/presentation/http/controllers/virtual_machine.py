from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends
from fastapi_error_map import ErrorAwareRouter
from pydantic import ValidationError
from starlette import status

from application.exceptions import (
    AccessDeniedError,
    CurrentUserDontAssignError,
    CurrentUserNotFound,
    GatewayFailedError,
    NoFreeVirtualMachinesError,
    VirtualMachineAlreadyExistsError,
    VirtualMachineClaimConflictError,
)
from domain.exceptions import DomainError, DomainFieldError
from presentation.exceptions import log_info
from presentation.handlers import (
    AddVirtualMachineHandler,
    ClaimVirtualMachineHandler,
    FreeVirtualMachineHandler,
)
from presentation.models import (
    VirtualMachineClaim,
    VirtualMachineClaimed,
    VirtualMachineCreate,
    VirtualMachineCreated,
)

from .dependencies import (
    authorize,
    authorize_by_activation_key,
    service_unavailable_rule,
)


def create_virtual_machine_router() -> APIRouter:
    router = ErrorAwareRouter(prefix="/virtual-machines", tags=["virtual-machines"])

    @router.post(
        "/",
        dependencies=[Depends(authorize)],
        error_map={
            ValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            DomainFieldError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            AccessDeniedError: status.HTTP_403_FORBIDDEN,
            CurrentUserDontAssignError: status.HTTP_401_UNAUTHORIZED,
            CurrentUserNotFound: status.HTTP_401_UNAUTHORIZED,
            VirtualMachineAlreadyExistsError: status.HTTP_409_CONFLICT,
            GatewayFailedError: service_unavailable_rule,
        },
        default_on_error=log_info,
        status_code=status.HTTP_201_CREATED,
        response_model=VirtualMachineCreated,
    )
    @inject
    async def add(
        request_body: VirtualMachineCreate,
        handler: FromDishka[AddVirtualMachineHandler],
    ):
        return await handler.execute(request_body)

    @router.post(
        "/claim",
        dependencies=[Depends(authorize_by_activation_key)],
        error_map={
            ValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            DomainFieldError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            DomainError: status.HTTP_409_CONFLICT,
            NoFreeVirtualMachinesError: status.HTTP_503_SERVICE_UNAVAILABLE,
            VirtualMachineClaimConflictError: status.HTTP_409_CONFLICT,
            CurrentUserDontAssignError: status.HTTP_401_UNAUTHORIZED,
            CurrentUserNotFound: status.HTTP_401_UNAUTHORIZED,
            GatewayFailedError: service_unavailable_rule,
        },
        default_on_error=log_info,
        status_code=status.HTTP_200_OK,
        response_model=VirtualMachineClaimed,
    )
    @inject
    async def claim(
        request_body: VirtualMachineClaim,
        handler: FromDishka[ClaimVirtualMachineHandler],
    ):
        return await handler.execute(request_body)

    @router.post(
        "/free",
        dependencies=[Depends(authorize)],
        error_map={
            ValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            AccessDeniedError: status.HTTP_403_FORBIDDEN,
            VirtualMachineClaimConflictError: status.HTTP_409_CONFLICT,
            CurrentUserDontAssignError: status.HTTP_401_UNAUTHORIZED,
            CurrentUserNotFound: status.HTTP_401_UNAUTHORIZED,
            GatewayFailedError: service_unavailable_rule,
        },
        default_on_error=log_info,
        status_code=status.HTTP_204_NO_CONTENT,
    )
    @inject
    async def free(handler: FromDishka[FreeVirtualMachineHandler]):
        await handler.execute()

    return router
