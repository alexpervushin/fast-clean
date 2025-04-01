from typing import Annotated, List
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, status

from microservices.shared.infrastructure.security.jwt_handler import JWTHandlerProtocol
from microservices.settings.application.commands import (
    AddDataSourceCommand,
    DeleteDataSourceCommand,
    UpdateDataSourceCommand,
)
from microservices.settings.application.dtos import (
    AddDataSourceInputDTO,
    DataSourceOutputDTO,
    UpdateDataSourceInputDTO,
)
from microservices.settings.application.queries import (
    GetDataSourceByIdQuery,
    ListDataSourcesQuery,
)
from microservices.shared.infrastructure.http.dependencies import (
    decode_token_and_get_user_id,
    get_validated_token,
)
from microservices.settings.presentation.rest.schemas import (
    AddDataSourceRequest,
    DataSourceResponse,
    ListDataSourcesResponse,
    UpdateDataSourceRequest,
)
from microservices.settings.presentation.rest.utils import mask_sensitive_config

router = APIRouter(prefix="/settings", tags=["settings"], route_class=DishkaRoute)


@router.post(
    "/sources",
    response_model=DataSourceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_data_source(
    token_str: Annotated[str, Depends(get_validated_token)],
    jwt_handler: FromDishka[JWTHandlerProtocol],
    body: AddDataSourceRequest,
    command: FromDishka[AddDataSourceCommand],
) -> DataSourceResponse:
    user_id = decode_token_and_get_user_id(token_str, jwt_handler)
    dto = AddDataSourceInputDTO(
        user_id=user_id,
        type=body.type,
        name=body.name,
        config=body.config,
        is_enabled=body.is_enabled,
    )
    result_dto: DataSourceOutputDTO = await command(dto)
    response_model = DataSourceResponse.model_validate(result_dto)
    response_model.config = mask_sensitive_config(response_model.config)
    return response_model


@router.get("/sources", response_model=ListDataSourcesResponse)
async def list_data_sources(
    token_str: Annotated[str, Depends(get_validated_token)],
    jwt_handler: FromDishka[JWTHandlerProtocol],
    query: FromDishka[ListDataSourcesQuery],
) -> ListDataSourcesResponse:
    user_id = decode_token_and_get_user_id(token_str, jwt_handler)
    result_dtos: List[DataSourceOutputDTO] = await query(user_id=user_id)
    response_data = []
    for dto in result_dtos:
        response_model = DataSourceResponse.model_validate(dto)
        response_model.config = mask_sensitive_config(response_model.config)
        response_data.append(response_model)
    return ListDataSourcesResponse(data=response_data)


@router.get("/sources/{source_id}", response_model=DataSourceResponse)
async def get_data_source_by_id(
    token_str: Annotated[str, Depends(get_validated_token)],
    jwt_handler: FromDishka[JWTHandlerProtocol],
    source_id: UUID,
    query: FromDishka[GetDataSourceByIdQuery],
) -> DataSourceResponse:
    user_id = decode_token_and_get_user_id(token_str, jwt_handler)
    result_dto: DataSourceOutputDTO = await query(source_id=source_id, user_id=user_id)
    response_model = DataSourceResponse.model_validate(result_dto)
    response_model.config = mask_sensitive_config(response_model.config)
    return response_model


@router.put("/sources/{source_id}", response_model=DataSourceResponse)
async def update_data_source(
    token_str: Annotated[str, Depends(get_validated_token)],
    jwt_handler: FromDishka[JWTHandlerProtocol],
    source_id: UUID,
    body: UpdateDataSourceRequest,
    command: FromDishka[UpdateDataSourceCommand],
) -> DataSourceResponse:
    user_id = decode_token_and_get_user_id(token_str, jwt_handler)


    dto = UpdateDataSourceInputDTO(
        name=body.name,
        config=body.config,
        is_enabled=body.is_enabled,
    )
    result_dto: DataSourceOutputDTO = await command(source_id=source_id, user_id=user_id, dto=dto)
    response_model = DataSourceResponse.model_validate(result_dto)
    response_model.config = mask_sensitive_config(response_model.config)
    return response_model


@router.delete("/sources/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data_source(
    token_str: Annotated[str, Depends(get_validated_token)],
    jwt_handler: FromDishka[JWTHandlerProtocol],
    source_id: UUID,
    command: FromDishka[DeleteDataSourceCommand],
) -> None:
    user_id = decode_token_and_get_user_id(token_str, jwt_handler)
    await command(source_id=source_id, user_id=user_id)
    return None