from application.compositions import AddVirtualMachineComposition
from application.usecase.add_virtual_machine import (
    AddVirtualMachineRequest,
    AddVirtualMachineResponse,
)
from presentation.models import VirtualMachineCreate, VirtualMachineCreated


class AddVirtualMachineHandler:
    def __init__(self, composition: AddVirtualMachineComposition):
        self._composition = composition

    async def execute(self, request: VirtualMachineCreate) -> VirtualMachineCreated:
        response: AddVirtualMachineResponse = await self._composition(
            AddVirtualMachineRequest.from_primitives(
                name=request.name,
                host=request.host,
                port=request.port,
                protocol=request.protocol,
            )
        )

        return VirtualMachineCreated(
            id=response.id.value,
            name=response.name,
            host=response.host,
            port=response.port,
            protocol=response.protocol,
            is_active=response.is_active,
        )
