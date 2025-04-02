from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from microservices.shared.infrastructure.config import Sentry


class CeleryBroker(BaseModel):
    url: str = "redis://localhost:6379/0"

class CeleryResultBackend(BaseModel):
    url: str = "redis://localhost:6379/1"

class CelerySettings(BaseModel):
    broker: CeleryBroker = CeleryBroker()
    result_backend: CeleryResultBackend = CeleryResultBackend()
    timezone: str = "UTC"

class Settings(BaseSettings):
    sentry: Sentry
    celery: CelerySettings = CelerySettings()

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )

def get_settings() -> Settings:
    return Settings() # noqa
