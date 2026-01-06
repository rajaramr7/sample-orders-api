"""Authentication routes."""

from fastapi import APIRouter, HTTPException, status

from ..auth import (
    authenticate_user,
    authenticate_client,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from ..models import TokenRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token", response_model=TokenResponse)
async def get_token(request: TokenRequest):
    """
    Get an access token using password or client_credentials grant.

    For password grant, provide username and password.
    For client_credentials grant, provide client_id and client_secret.
    """
    if request.grant_type == "password":
        if not request.username or not request.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username and password required for password grant"
            )

        user = authenticate_user(request.username, request.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(
            data={"sub": user["user_id"], "role": user["role"]}
        )

    elif request.grant_type == "client_credentials":
        if not request.client_id or not request.client_secret:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client ID and secret required for client_credentials grant"
            )

        client = authenticate_client(request.client_id, request.client_secret)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid client credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(
            data={"sub": client["user_id"], "role": client["role"]}
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported grant type"
        )

    return TokenResponse(
        access_token=access_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
