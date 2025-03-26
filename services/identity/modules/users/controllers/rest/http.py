from dishka import FromDishka
from fastapi import APIRouter
from schemas import CreateUserRequest

from services.identity.modules.users.application.dtos import (
    CreateUserInputDTO,
    UpdateUserInputDTO,
)
from services.identity.modules.users.application.services import UserService
from services.identity.modules.users.controllers.rest.schemas import UpdateUserRequest

router = APIRouter(prefix="/users", tags=["users"])


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
) -> None:
    dto = UpdateUserInputDTO(name=body.name, email=str(body.email))
    return await service.update_user(dto, user_id)

