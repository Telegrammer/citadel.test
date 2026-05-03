import logging

from application.events import VirtualMachineFreed
from application.ports import UnitOfWork
from application.ports.notifiers import VirtualMachineFreedNotifier
from application.usecase.free_virtual_machine import (
    FreeVirtualMachineResponse,
    FreeVirtualMachineUsecase,
)


logger = logging.getLogger(__name__)


class FreeVirtualMachineComposition:
    def __init__(
        self,
        usecase: FreeVirtualMachineUsecase,
        unit_of_work: UnitOfWork,
        notifier: VirtualMachineFreedNotifier,
    ):
        self._usecase = usecase
        self._unit_of_work = unit_of_work
        self._notifier = notifier

    async def __call__(self) -> None:
        logger.info("Начато освобождение всех занятых виртуальных машин")

        async with self._unit_of_work:
            response: FreeVirtualMachineResponse = await self._usecase()

        for user_id in response.freed_user_ids:
            await self._notifier.notify(VirtualMachineFreed(user_id=user_id))

        logger.info(
            "Освобождено виртуальных машин: %s",
            len(response.freed_user_ids),
        )
