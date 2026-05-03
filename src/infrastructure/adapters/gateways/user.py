from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.exceptions import UserAlreadyExistsError
from domain.entities.user import User, UserId
from domain.value_objects import EmailAddress
from infrastructure.exceptions import gateway_failed_aware, unique_violation_aware
from infrastructure.models.sqlalchemy import User as ORMUser

from ..mappers import SQLAlchemyUserMapper


class SQLAlchemyUserCommandGateway:
    def __init__(self, session: AsyncSession, mapper: SQLAlchemyUserMapper) -> None:
        self._session = session
        self._mapper = mapper

    @gateway_failed_aware("Не удалось сохранить пользователя")
    @unique_violation_aware(
        {
            "users_pkey": ("user_exists", "Пользователь с таким id уже существует"),
            "users_email_key": (
                "user_exists",
                "Пользователь с таким email уже существует",
            ),
            "users_activation_key_lookup_key": (
                "user_activation_key_exists",
                "Ключ активации уже существует",
            ),
        },
        UserAlreadyExistsError,
    )
    async def add(self, user: User) -> None:
        self._session.add(self._mapper.to_dto(user))
        await self._session.flush()

    @gateway_failed_aware("Не удалось обновить пользователя")
    async def update(self, user: User) -> None:
        await self._session.merge(self._mapper.to_dto(user))
        await self._session.flush()


class SQLAlchemyUserQueryGateway:
    def __init__(self, session: AsyncSession, mapper: SQLAlchemyUserMapper) -> None:
        self._session = session
        self._mapper = mapper

    @gateway_failed_aware("Не удалось получить пользователя по email")
    async def by_email(self, email: EmailAddress) -> User | None:
        stmt = select(ORMUser).where(ORMUser.email == email.value)
        dto = (await self._session.execute(stmt)).scalar_one_or_none()
        return self._mapper.to_domain(dto) if dto else None

    @gateway_failed_aware("Не удалось получить пользователя по id")
    async def by_id(self, user_id: UserId) -> User | None:
        stmt = select(ORMUser).where(ORMUser.id == user_id.value)
        dto = (await self._session.execute(stmt)).scalar_one_or_none()
        return self._mapper.to_domain(dto) if dto else None

    @gateway_failed_aware("Не удалось получить пользователя по ключу активации")
    async def by_activation_key_lookup(self, lookup: str) -> User | None:
        stmt = select(ORMUser).where(ORMUser.activation_key_lookup == lookup)
        dto = (await self._session.execute(stmt)).scalar_one_or_none()
        return self._mapper.to_domain(dto) if dto else None
