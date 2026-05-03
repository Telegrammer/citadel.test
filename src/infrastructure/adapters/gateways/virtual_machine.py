from sqlalchemy import inspect as sqlalchemy_inspect
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.exceptions import (
    VirtualMachineAlreadyExistsError,
    VirtualMachineClaimConflictError,
)
from domain.entities.user import UserId
from domain.entities.virtual_machine import VirtualMachine, VirtualMachineId
from infrastructure.exceptions import (
    gateway_failed_aware,
    stale_data_aware,
    unique_violation_aware,
)
from infrastructure.models.sqlalchemy import VirtualMachine as ORMVirtualMachine

from ..mappers import SQLAlchemyVirtualMachineMapper


def _virtual_machine_claim_conflict() -> VirtualMachineClaimConflictError:
    return VirtualMachineClaimConflictError(
        "virtual_machine_claim_conflict",
        "Виртуальная машина была занята параллельным запросом",
    )


class SQLAlchemyVirtualMachineCommandGateway:
    def __init__(
        self, session: AsyncSession, mapper: SQLAlchemyVirtualMachineMapper
    ) -> None:
        self._session = session
        self._mapper = mapper

    @gateway_failed_aware("Не удалось сохранить виртуальную машину")
    @unique_violation_aware(
        {
            "virtual_machines_pkey": (
                "virtual_machine_exists",
                "Виртуальная машина с таким id уже существует",
            )
        },
        VirtualMachineAlreadyExistsError,
    )
    async def add(self, virtual_machine: VirtualMachine) -> None:
        self._session.add(self._mapper.to_dto(virtual_machine))
        await self._session.flush()

    @gateway_failed_aware("Не удалось обновить виртуальную машину")
    @stale_data_aware(_virtual_machine_claim_conflict)
    async def update(self, virtual_machine: VirtualMachine) -> None:
        dto = self._mapper.to_dto(virtual_machine)
        state = sqlalchemy_inspect(dto)

        if state.transient or state.detached:
            await self._session.merge(dto)

        await self._session.flush()

    @gateway_failed_aware("Не удалось освободить виртуальные машины")
    async def release_all_assigned(self) -> list[UserId]:
        to_free = (
            select(
                ORMVirtualMachine.id.label("id"),
                ORMVirtualMachine.current_user_id.label("old_user_id"),
            )
            .where(ORMVirtualMachine.current_user_id.is_not(None))
            .cte("to_free")
        )
        stmt = (
            update(ORMVirtualMachine)
            .add_cte(to_free)
            .where(ORMVirtualMachine.id == to_free.c.id)
            .values(
                current_user_id=None,
                version=ORMVirtualMachine.version + 1,
            )
            .returning(to_free.c.old_user_id)
        )
        result = await self._session.execute(stmt)
        rows = result.fetchall()
        return [UserId(row[0]) for row in rows]


class SQLAlchemyVirtualMachineQueryGateway:
    def __init__(
        self, session: AsyncSession, mapper: SQLAlchemyVirtualMachineMapper
    ) -> None:
        self._session = session
        self._mapper = mapper

    @gateway_failed_aware("Не удалось получить виртуальную машину по id")
    async def by_id(
        self, virtual_machine_id: VirtualMachineId
    ) -> VirtualMachine | None:
        stmt = select(ORMVirtualMachine).where(
            ORMVirtualMachine.id == virtual_machine_id.value
        )
        dto = (await self._session.execute(stmt)).scalar_one_or_none()
        return self._mapper.to_domain(dto) if dto else None

    async def by_availability(self) -> VirtualMachine | None:
        stmt = (
            select(ORMVirtualMachine)
            .where(ORMVirtualMachine.is_active.is_(True))
            .where(ORMVirtualMachine.current_user_id.is_(None))
            .order_by(ORMVirtualMachine.last_used_at.asc().nullsfirst())
            .limit(1)
        )
        dto = (await self._session.execute(stmt)).scalar_one_or_none()
        return self._mapper.to_domain(dto) if dto else None

    @gateway_failed_aware("Не удалось получить виртуальную машину пользователя")
    async def by_user(self, user_id: UserId) -> VirtualMachine | None:
        stmt = select(ORMVirtualMachine).where(
            ORMVirtualMachine.current_user_id == user_id.value
        )
        dto = (await self._session.execute(stmt)).scalar_one_or_none()
        return self._mapper.to_domain(dto) if dto else None
