from dishka import FromDishka
from fastapi import APIRouter
from schemas import CreateUserRequest
from services.identity.modules.users.application.dtos import CreateUserDTO
from services.identity.modules.users.application.services import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", status_code=201)
async def register_user(service: FromDishka[UserService], user: CreateUserRequest) -> None:
    dto = CreateUserDTO(name=user.name, email=user.email, password=user.password)
    return await service.register_user(dto)

@router.put("/{user_id}", status_code=200)
async def update_user(service: FromDishka[UserService], user_id: str, user: CreateUserRequest) -> None:
    dto = CreateUserDTO(name=user.name, email=user.email, password=user.password)
    return await service.update_user(dto, user_id)

