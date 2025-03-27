from dishka import make_async_container

from services.shared.infrastructure.di.providers import (
    SharedDatabaseProvider,
    SharedIdGeneratorProvider,
    SharedPasswordHasherProvider,
)
from services.users.infrastructure.di.providers import ConfigProvider, UserProvider

container = make_async_container(
    ConfigProvider(),
    SharedDatabaseProvider(),
    SharedPasswordHasherProvider(),
    SharedIdGeneratorProvider(),
    UserProvider(),
)