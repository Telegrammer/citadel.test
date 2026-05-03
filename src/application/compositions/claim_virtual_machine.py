import logging

from application.events import VirtualMachineClaimed
from application.exceptions import VirtualMachineClaimConflictError, retry_on_conflict
from application.ports import UnitOfWork
from application.ports.notifiers import VirtualMachineClaimedNotifier
from application.usecase.claim_virtual_machine import (
    ClaimVirtualMachineRequest,
    ClaimVirtualMachineResponse,
    ClaimVirtualMachineUsecase,
)


logger = logging.getLogger(__name__)


class ClaimVirtualMachineComposition:
    def __init__(
        self,
        usecase: ClaimVirtualMachineUsecase,
        unit_of_work: UnitOfWork,
        notifier: VirtualMachineClaimedNotifier,
    ):
        self._usecase = usecase
        self._unit_of_work = unit_of_work
        self._notifier = notifier

    @retry_on_conflict(VirtualMachineClaimConflictError)
    async def __call__(
        self, request: ClaimVirtualMachineRequest
    ) -> ClaimVirtualMachineResponse:

        logger.info("Начато получение виртуальной машины")

        async with self._unit_of_work:
            response: ClaimVirtualMachineResponse = await self._usecase(request)

        await self._notifier.notify(
            VirtualMachineClaimed(
                user_id=response.user_id,
                host=response.host,
                port=response.port,
                protocol=response.protocol,
            )
        )
        logger.info("Виртуальная машина получена %s:%s", response.host, response.port)

        return response
