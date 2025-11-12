from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core.auth import require_auth
from app.core.config import settings
from app.core.exceptions import SupabaseAuthError, ValidationError
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


@router.get("/me", response_model=UserPublic, operation_id="getCurrentUser")
async def get_current_user_info(
    authenticated_user: Annotated[User, Depends(require_auth)],
) -> UserPublic:
    return UserPublic.model_validate(authenticated_user)


@router.post("/login", response_model=LoginResponse, operation_id="login")
async def login_with_cookie(
    token_request: TokenRequest,
    response: Response,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> LoginResponse:
    try:
        user = await auth_service.authenticate_with_supabase(token_request.token)

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
    except SupabaseAuthError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/refresh", response_model=RefreshResponse, operation_id="refreshToken")
async def refresh_token(
    response: Response,
    authenticated_user: Annotated[User, Depends(require_auth)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RefreshResponse:
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


@router.delete("/logout", response_model=LogoutResponse, operation_id="logout")
async def logout(response: Response) -> LogoutResponse:
    response.delete_cookie(
        key=settings.API_JWT_COOKIE_NAME,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
    )

    return LogoutResponse(message="Logged out successfully")
