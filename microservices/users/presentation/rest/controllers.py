from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from microservices.users.application.dtos import (
    CreateUserInputDTO,
    UpdateUserInputDTO,
)
from microservices.users.application.services import UserService
from microservices.users.presentation.rest.schemas import (
    CreateUserRequest,
    UpdateUserRequest,
    UpdateUserResponse,
)

router = APIRouter(prefix="/users", tags=["users"], route_class=DishkaRoute)


@router.post("", status_code=status.HTTP_201_CREATED)
async def register_user(
    service: FromDishka[UserService], body: CreateUserRequest
) -> None:
    dto = CreateUserInputDTO(
        name=body.name, email=str(body.email), password=body.password
    )
    await service.register_user(dto)


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    service: FromDishka[UserService], user_id: UUID, body: UpdateUserRequest
) -> UpdateUserResponse:
    dto = UpdateUserInputDTO(
        name=body.name, email=str(body.email) if body.email else None
    )
    result = await service.update_user(dto, user_id)
    return UpdateUserResponse(name=result.name, email=result.email)