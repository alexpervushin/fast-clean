from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, HTTPException, status

from microservices.shared.domain.exceptions import AuthenticationError
from microservices.shared.infrastructure.security.jwt_handler import JWTHandlerProtocol
from microservices.users.application.dtos import (
    CreateUserInputDTO,
    UpdateUserInputDTO,
)
from microservices.users.application.user_service import UserService
from microservices.users.domain.repositories import UserRepositoryProtocol
from microservices.users.presentation.rest.dependencies import get_token_credentials
from microservices.users.presentation.rest.schemas import (
    CreateUserRequest,
    UpdateUserRequest,
    UpdateUserResponse,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["users"], route_class=DishkaRoute)

# TODO: refactor

@router.post("", status_code=status.HTTP_201_CREATED)
async def register_user(
    service: FromDishka[UserService], body: CreateUserRequest
) -> None:
    dto = CreateUserInputDTO(
        name=body.name, email=str(body.email), password=body.password
    )
    await service.register_user(dto)


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    token_credentials: Annotated[str, Depends(get_token_credentials)],
    jwt_handler: FromDishka[JWTHandlerProtocol],
    user_repo: FromDishka[UserRepositoryProtocol]
) -> UserResponse:
    try:
        current_user_id = jwt_handler.decode_token(token_credentials)
    except AuthenticationError as e:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    user = await user_repo.get_by_id(current_user_id)
    return UserResponse(id=user.id, name=user.name, email=user.email)


@router.put("/me", response_model=UpdateUserResponse)
async def update_current_user(
    body: UpdateUserRequest,
    token_credentials: Annotated[str, Depends(get_token_credentials)],
    jwt_handler: FromDishka[JWTHandlerProtocol],
    service: FromDishka[UserService],
) -> UpdateUserResponse:
    try:
        current_user_id = jwt_handler.decode_token(token_credentials)
    except AuthenticationError as e:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    dto = UpdateUserInputDTO(
        name=body.name, email=str(body.email) if body.email else None
    )
    result = await service.update_user(dto, current_user_id)
    return UpdateUserResponse(name=result.name, email=result.email)