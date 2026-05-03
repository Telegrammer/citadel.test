from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Union
from uuid import uuid4

import sqlalchemy as sa
from alembic import op
from passlib.context import CryptContext

revision: str = "a9b8c7d6"
down_revision: Union[str, Sequence[str], None] = "6f2a1b0c3d4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_dotenv_file() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    env_path = _repo_root() / ".env"
    if env_path.is_file():
        load_dotenv(env_path, override=False)


def _bootstrap_credentials() -> tuple[str | None, str | None]:
    _load_dotenv_file()
    import os

    email = (os.environ.get("APP_CONFIG__BOOTSTRAP_ADMIN__EMAIL") or "").strip() or None
    raw_pw = os.environ.get("APP_CONFIG__BOOTSTRAP_ADMIN__PASSWORD")
    password: str | None
    if raw_pw is None:
        password = None
    else:
        password = raw_pw.strip() or None

    if email and password:
        return email, password

    from setup.config import Settings

    s = Settings()
    e2 = (s.bootstrap_admin.email or "").strip() or None
    p2 = s.bootstrap_admin.password
    if p2 is not None:
        p2 = p2.strip() or None
    return e2, p2


def upgrade() -> None:
    email, password = _bootstrap_credentials()
    if not email or not password:
        return

    ctx = CryptContext(schemes=["bcrypt"])
    pw_hash = bytes(ctx.hash(password), encoding="utf-8")
    now = datetime.now(UTC)
    user_id = uuid4()

    exists = op.get_bind().execute(
        sa.text("SELECT 1 FROM users WHERE email = :email LIMIT 1").bindparams(email=email)
    ).scalar()
    if exists:
        return

    op.execute(
        sa.text(
            """
            INSERT INTO users (
                id, created_at, updated_at, email, password,
                activation_key_lookup, activation_key, activation_key_expires,
                is_active, is_admin
            )
            VALUES (
                :id, :created_at, :updated_at, :email, :password,
                NULL, NULL, NULL,
                true, true
            )
            """
        ).bindparams(
            id=user_id,
            created_at=now,
            updated_at=now,
            email=email,
            password=pw_hash,
        )
    )


def downgrade() -> None:
    email, _password = _bootstrap_credentials()
    if not email:
        return

    op.execute(
        sa.text("DELETE FROM users WHERE email = :email AND is_admin = true").bindparams(
            email=email
        )
    )
