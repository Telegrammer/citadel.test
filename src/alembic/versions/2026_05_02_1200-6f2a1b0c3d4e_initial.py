from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "6f2a1b0c3d4e"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    protocol_enum = postgresql.ENUM(
        "http",
        "socks5",
        "https",
        name="virtual_machine_protocol",
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.LargeBinary(), nullable=False),
        sa.Column("activation_key_lookup", sa.String(), nullable=True),
        sa.Column("activation_key", sa.LargeBinary(), nullable=True),
        sa.Column("activation_key_expires", sa.DateTime(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_users"),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.UniqueConstraint("activation_key_lookup", name="uq_users_activation_key_lookup"),
    )

    op.create_table(
        "virtual_machines",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("host", sa.String(), nullable=False),
        sa.Column("port", sa.Integer(), nullable=False),
        sa.Column("protocol", protocol_enum, nullable=False),
        sa.Column("current_user_id", sa.Uuid(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("last_used_at", sa.DateTime(), nullable=True),
        sa.Column("version", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.ForeignKeyConstraint(
            ["current_user_id"],
            ["users.id"],
            name="fk_virtual_machines_current_user_id_users",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_virtual_machines"),
    )


def downgrade() -> None:
    op.drop_table("virtual_machines")
    op.drop_table("users")
    protocol_enum = postgresql.ENUM(
        "http",
        "socks5",
        "https",
        name="virtual_machine_protocol",
    )
    protocol_enum.drop(op.get_bind(), checkfirst=True)
