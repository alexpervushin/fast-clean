from dishka import Provider, Scope, make_async_container, provide
from pydantic_settings import BaseSettings

from microservices.shared.domain.ports import IdGeneratorProtocol
from microservices.shared.infrastructure.database.session import (
    AsyncSessionProtocol,
    TransactionManager,
)
from microservices.shared.infrastructure.di.providers import (
    SharedDatabaseProvider,
    SharedIdGeneratorProvider,
    SharedSecurityProvider,
)
from microservices.settings.application.commands import (
    AddDataSourceCommand,
    DeleteDataSourceCommand,
    UpdateDataSourceCommand,
)
from microservices.settings.application.queries import (
    GetDataSourceByIdQuery,
    ListDataSourcesQuery,
)
from microservices.settings.domain.ports import DataSourceRepositoryProtocol
from microservices.settings.infrastructure.config import Settings, get_settings
from microservices.settings.infrastructure.persistence.repositories import (
    DataSourceRepository,
)


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_settings(self) -> Settings:
        return get_settings()

    @provide(scope=Scope.APP)
    async def provide_base_settings(self, settings: Settings) -> BaseSettings:
        return settings


class SettingsProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_data_source_repository(
        self, session: AsyncSessionProtocol
    ) -> DataSourceRepositoryProtocol:
        return DataSourceRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_add_data_source_command(
        self,
        repository: DataSourceRepositoryProtocol,
        id_generator: IdGeneratorProtocol,
        transaction_manager: TransactionManager,
    ) -> AddDataSourceCommand:
        return AddDataSourceCommand(
            repository=repository,
            id_generator=id_generator,
            transaction_manager=transaction_manager,
        )

    @provide(scope=Scope.REQUEST)
    def get_update_data_source_command(
        self,
        repository: DataSourceRepositoryProtocol,
        transaction_manager: TransactionManager,
    ) -> UpdateDataSourceCommand:
        return UpdateDataSourceCommand(
            repository=repository,
            transaction_manager=transaction_manager,
        )

    @provide(scope=Scope.REQUEST)
    def get_delete_data_source_command(
        self,
        repository: DataSourceRepositoryProtocol,
        transaction_manager: TransactionManager,
    ) -> DeleteDataSourceCommand:
        return DeleteDataSourceCommand(
            repository=repository,
            transaction_manager=transaction_manager,
        )

    @provide(scope=Scope.REQUEST)
    def get_data_source_by_id_query(
        self,
        repository: DataSourceRepositoryProtocol,
    ) -> GetDataSourceByIdQuery:
        return GetDataSourceByIdQuery(repository=repository)

    @provide(scope=Scope.REQUEST)
    def get_list_data_sources_query(
        self,
        repository: DataSourceRepositoryProtocol,
    ) -> ListDataSourcesQuery:
        return ListDataSourcesQuery(repository=repository)


container = make_async_container(
    ConfigProvider(),
    SharedDatabaseProvider(),
    SharedSecurityProvider(),
    SharedIdGeneratorProvider(),
    SettingsProvider(),
)