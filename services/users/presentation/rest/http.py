from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from services.users.application.dtos import (
    CreateUserInputDTO,
    UpdateUserInputDTO,
)
from services.users.application.user_services import UserService
from services.users.presentation.rest.schemas import (
    CreateUserRequest,
    UpdateUserRequest,
    UpdateUserResponse,
)

router = APIRouter(prefix="/users", tags=["users"], route_class=DishkaRoute)


@router.post("", status_code=201)
async def register_user(
    service: FromDishka[UserService], body: CreateUserRequest
) -> None:
    dto = CreateUserInputDTO(
        name=body.name, email=str(body.email), password=body.password
    )
    return await service.register_user(dto)


@router.put("/{user_id}", status_code=200)
async def update_user(
    service: FromDishka[UserService], user_id: str, body: UpdateUserRequest
) -> UpdateUserResponse:
    dto = UpdateUserInputDTO(name=body.name, email=str(body.email))
    result = await service.update_user(dto, user_id)
    return UpdateUserResponse(name=result.name, email=result.email)