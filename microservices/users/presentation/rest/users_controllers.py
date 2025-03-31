from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, status

from microservices.shared.infrastructure.security.jwt_handler import (
    JWTHandlerProtocol,
)
from microservices.users.application.commands import (
    RegisterUserCommand,
    UpdateUserCommand,
)
from microservices.users.application.dtos import (
    CreateUserInputDTO,
    UpdateUserInputDTO,
)
from microservices.users.application.queries import GetUserByIdQuery
from microservices.users.presentation.rest.dependencies import (
    decode_token_and_get_user_id,
    get_validated_token,
)
from microservices.users.presentation.rest.schemas import (
    CreateUserRequest,
    UpdateUserRequest,
    UpdateUserResponse,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["users"], route_class=DishkaRoute)


@router.post("", status_code=status.HTTP_201_CREATED)
async def register_user(
    command: FromDishka[RegisterUserCommand],
    body: CreateUserRequest
) -> None:
    dto = CreateUserInputDTO(
        name=body.name, email=str(body.email), password=body.password
    )
    await command(dto)


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    token_str: Annotated[str, Depends(get_validated_token)],
    jwt_handler: FromDishka[JWTHandlerProtocol],
    query: FromDishka[GetUserByIdQuery],
) -> UserResponse:
    current_user_id = decode_token_and_get_user_id(token_str, jwt_handler)
    user_dto = await query(user_id=current_user_id)
    return UserResponse(id=user_dto.id, name=user_dto.name, email=user_dto.email)


@router.put("/me", response_model=UpdateUserResponse)
async def update_current_user(
    body: UpdateUserRequest,
    token_str: Annotated[str, Depends(get_validated_token)],
    jwt_handler: FromDishka[JWTHandlerProtocol],
    command: FromDishka[UpdateUserCommand],
) -> UpdateUserResponse:
    current_user_id = decode_token_and_get_user_id(token_str, jwt_handler)
    dto = UpdateUserInputDTO(
        name=body.name, email=str(body.email) if body.email else None
    )
    result_dto = await command(user_id=current_user_id, dto=dto)
    return UpdateUserResponse(name=result_dto.name, email=result_dto.email)