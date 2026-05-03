from datetime import datetime
from uuid import UUID
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from domain.entities.virtual_machine import ConnectionProtocol

from .base import Base


class VirtualMachine(Base):
    id: Mapped[UUID] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=False)
    host: Mapped[str] = mapped_column(nullable=False)
    port: Mapped[int] = mapped_column(nullable=False)
    protocol: Mapped[ConnectionProtocol] = mapped_column(
        Enum(
            ConnectionProtocol,
            name="virtual_machine_protocol",
            values_callable=lambda enum: [item.value for item in enum],
        ),
        nullable=False,
    )
    current_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(nullable=False)
    last_used_at: Mapped[datetime | None] = mapped_column(nullable=True)
    version: Mapped[int] = mapped_column(nullable=False, default=1, server_default="1")

    __mapper_args__ = {"version_id_col": version}
