from datetime import timedelta

from application.compositions import ClaimVirtualMachineComposition
from application.usecase.claim_virtual_machine import (
    ClaimVirtualMachineRequest,
    ClaimVirtualMachineResponse,
)
from presentation.models import VirtualMachineClaim, VirtualMachineClaimed
from presentation.presenters import JwtAuthPresenter


class ClaimVirtualMachineHandler:
    def __init__(
        self,
        composition: ClaimVirtualMachineComposition,
        auth_presenter: JwtAuthPresenter,
        login_duration: timedelta,
    ):
        self._composition = composition
        self._auth_presenter = auth_presenter
        self._login_duration = login_duration

    async def execute(self, request: VirtualMachineClaim) -> VirtualMachineClaimed:
        response: ClaimVirtualMachineResponse = await self._composition(
            ClaimVirtualMachineRequest.from_primitives(
                activation_key=request.activation_key,
            )
        )

        return VirtualMachineClaimed(
            user_id=response.user_id.value,
            host=response.host,
            port=response.port,
            protocol=response.protocol,
            access_token=self._auth_presenter.encode_access_token(
                user_id=response.user_id,
                issued_at=response.claimed_at,
                duration=self._login_duration,
            ),
        )
