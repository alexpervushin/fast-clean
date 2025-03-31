from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

token_auth_scheme = HTTPBearer()


async def get_token_credentials(
    token: Annotated[HTTPBearer, Depends(token_auth_scheme)],
) -> str:
    if not token or not token.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token.credentials

