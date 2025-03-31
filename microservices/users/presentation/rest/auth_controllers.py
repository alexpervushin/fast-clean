from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from microservices.users.application.auth_service import AuthService
from microservices.users.presentation.rest.schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute)


@router.post("/login", response_model=TokenResponse)
async def login_for_access_token(
    auth_service: FromDishka[AuthService], body: LoginRequest
) -> TokenResponse:
    access_token = await auth_service.authenticate_user(
        email=str(body.email), password=body.password
    )
    return TokenResponse(access_token=access_token)