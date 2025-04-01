from pydantic_settings import BaseSettings, SettingsConfigDict

from microservices.shared.infrastructure.config import (
    JWT,
    Postgres,
    Sentry,
    Server,
)


class Settings(BaseSettings):
    sentry: Sentry
    postgres: Postgres
    server: Server
    jwt: JWT

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )


def get_settings() -> Settings:
    return Settings() # noqa
