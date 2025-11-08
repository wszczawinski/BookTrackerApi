from fastapi import APIRouter, Depends, HTTPException, Response

from app.core.auth import require_auth
from app.core.config import settings
from app.models.domain.user import User
from app.models.requests import TokenRequest
from app.models.responses import (
    LoginResponse,
    LogoutResponse,
    RefreshResponse,
    UserPublic,
)
from app.services.auth_service import AuthService
from app.services.dependencies import get_auth_service

router = APIRouter()


@router.get("/me", response_model=UserPublic)
async def get_current_user_info(authenticated_user: User = Depends(require_auth)):
    return UserPublic.model_validate(authenticated_user)


@router.post("/login", response_model=LoginResponse)
async def login_with_cookie(
    token_request: TokenRequest,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    user = await auth_service.authenticate_with_supabase(token_request.token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Supabase token")
    api_jwt, expires_at = auth_service.create_api_jwt(user.id)

    response.set_cookie(
        key=settings.API_JWT_COOKIE_NAME,
        value=api_jwt,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",  # HTTPS
        samesite="lax",
        max_age=settings.API_JWT_EXPIRE_HOURS * 60 * 60,  # Convert hours to seconds
    )

    return LoginResponse(
        message="Logged in successfully",
        user=UserPublic.model_validate(user),
        expires_at=expires_at,
    )


@router.post("/refresh", response_model=RefreshResponse)
async def refresh_token(
    response: Response,
    authenticated_user: User = Depends(require_auth),
    auth_service: AuthService = Depends(get_auth_service),
):
    new_jwt, expires_at = auth_service.create_api_jwt(authenticated_user.id)

    response.set_cookie(
        key=settings.API_JWT_COOKIE_NAME,
        value=new_jwt,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",  # HTTPS
        samesite="lax",
        max_age=settings.API_JWT_EXPIRE_HOURS * 60 * 60,  # In seconds
    )

    return RefreshResponse(
        message="Token refreshed successfully", expires_at=expires_at
    )


@router.delete("/logout", response_model=LogoutResponse)
async def logout(response: Response):
    response.delete_cookie(
        key=settings.API_JWT_COOKIE_NAME,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
    )

    return LogoutResponse(message="Logged out successfully")
