import logging

from application.ports import UnitOfWork
from application.usecase.add_virtual_machine import (
    AddVirtualMachineRequest,
    AddVirtualMachineResponse,
    AddVirtualMachineUsecase,
)


logger = logging.getLogger(__name__)


class AddVirtualMachineComposition:
    def __init__(self, usecase: AddVirtualMachineUsecase, unit_of_work: UnitOfWork):
        self._usecase = usecase
        self._unit_of_work = unit_of_work

    async def __call__(
        self, request: AddVirtualMachineRequest
    ) -> AddVirtualMachineResponse:

        logger.info("Начато добавление виртуальной машины")

        async with self._unit_of_work:
            response: AddVirtualMachineResponse = await self._usecase(request)

        logger.info("Виртуальная машина добавлена %s", response.id)

        return response
