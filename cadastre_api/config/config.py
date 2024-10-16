from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

MINUTES = 10
REFRESH_MINUTES = 30


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_pre_ping: bool = True
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AuthConfig(BaseModel):
    secret: str
    algorithm: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_file=".env",
    )
    run: RunConfig = RunConfig()
    db: DatabaseConfig
    auth: AuthConfig


settings = Settings()
