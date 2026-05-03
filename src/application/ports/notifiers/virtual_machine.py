from application.events import VirtualMachineClaimed, VirtualMachineFreed


class VirtualMachineClaimedNotifier:
    async def notify(self, event: VirtualMachineClaimed) -> bool:
        return True


class VirtualMachineFreedNotifier:
    async def notify(self, event: VirtualMachineFreed) -> bool:
        return True
