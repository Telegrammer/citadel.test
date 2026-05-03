from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import mapped_column, Mapped


from .base import Base


class User(Base):
    id: Mapped[UUID] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(nullable=False)
    activation_key_lookup: Mapped[str | None] = mapped_column(unique=True, nullable=True)
    activation_key: Mapped[bytes | None] = mapped_column(nullable=True)
    activation_key_expires: Mapped[datetime | None] = mapped_column(nullable=True)

    is_active: Mapped[bool] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(nullable=False)
