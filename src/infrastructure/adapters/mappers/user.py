from domain.entities.user import ActivationKey, User, UserId
from domain.value_objects import EmailAddress
from infrastructure.models.sqlalchemy import User as ORMUser


class SQLAlchemyUserMapper:
    def to_dto(self, domain: User) -> ORMUser:
        return ORMUser(
            id=domain.id.value,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            email=domain.email.value,
            password=domain.password,
            activation_key_lookup=domain.activation_key.lookup
            if domain.activation_key
            else None,
            activation_key=domain.activation_key.value
            if domain.activation_key
            else None,
            activation_key_expires=domain.activation_key.expire_at
            if domain.activation_key
            else None,
            is_active=domain.is_active,
            is_admin=domain.is_admin,
        )

    def to_domain(self, dto: ORMUser) -> User:
        return User(
            id=UserId(dto.id),
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            email=EmailAddress(dto.email),
            password=dto.password,
            activation_key=ActivationKey(
                lookup=dto.activation_key_lookup,
                value=dto.activation_key,
                expire_at=dto.activation_key_expires,
            )
            if dto.activation_key and dto.activation_key_lookup
            else None,
            is_active=dto.is_active,
            is_admin=dto.is_admin,
        )
