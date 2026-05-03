from application.compositions import FreeVirtualMachineComposition


class FreeVirtualMachineHandler:
    def __init__(self, composition: FreeVirtualMachineComposition):
        self._composition = composition

    async def execute(self) -> None:
        await self._composition()
