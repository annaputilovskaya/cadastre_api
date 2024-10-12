from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import  BaseSettings, SettingsConfigDict


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


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_file=".env",
    )
    run:  RunConfig = RunConfig()
    db: DatabaseConfig


settings = Settings()
