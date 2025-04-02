from dishka import Provider, Scope, make_async_container, provide
from pydantic_settings import BaseSettings

from microservices.scheduler.infrastructure.config import Settings, get_settings

class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_settings(self) -> Settings:
        return get_settings()

    @provide(scope=Scope.APP)
    def provide_base_settings(self, settings: Settings) -> BaseSettings:
        return settings

container = make_async_container(
    ConfigProvider(),
)