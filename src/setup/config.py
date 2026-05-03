from pathlib import Path

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent.parent


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class DatabaseConfig(BaseModel):
    user: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: int = 5432
    name: str = "citadel"
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: str | None = None

    @property
    def url(self) -> str:
        auth = f":{self.password}@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.db}"


class CeleryConfig(BaseModel):
    broker_url: str | None = None
    result_backend: str | None = None


class SMTPConfig(BaseModel):
    host: str = "localhost"
    port: int = 1025
    sender_email: str = "noreply@citadel.local"
    username: str | None = None
    password: str | None = None
    use_tls: bool = False
    timeout: float = 10.0


class AuthConfig(BaseModel):
    secret_key: Path = BASE_DIR / "certificates" / "jwt-private.pem"
    public_key: Path = BASE_DIR / "certificates" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 30

    @field_validator("algorithm")
    @classmethod
    def validate_algorithm(cls, value: str) -> str:
        allowed = {"RS256"}
        if value not in allowed:
            raise ValueError(f'JWT algorithm "{value}" is not allowed: {", ".join(sorted(allowed))}')
        return value


class ServiceConfig(BaseModel):
    login_duration_minutes: int = 30
    activation_key_expiration_minutes: int = 30
    dummy_password: str = "DummyPassword1!"


class CORSConfig(BaseModel):
    allow_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    )


class BootstrapAdminConfig(BaseModel):

    email: str | None = None
    password: str | None = None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    run: RunConfig = RunConfig()
    db: DatabaseConfig = DatabaseConfig()
    redis: RedisConfig = RedisConfig()
    celery: CeleryConfig = CeleryConfig()
    smtp: SMTPConfig = SMTPConfig()
    auth: AuthConfig = AuthConfig()
    service: ServiceConfig = ServiceConfig()
    cors: CORSConfig = CORSConfig()
    bootstrap_admin: BootstrapAdminConfig = Field(default_factory=BootstrapAdminConfig)


settings = Settings()
