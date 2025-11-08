from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from app.core.config import settings
from app.core.permissions import Permission, user_has_permission
from app.models.domain.user import User
from app.services.auth_service import AuthService
from app.services.dependencies import get_auth_service


class AuthorizationError(HTTPException):
    def __init__(self, detail: str = "Not authorized"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


async def require_auth(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    token = request.cookies.get(settings.API_JWT_COOKIE_NAME)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required - please login",
        )

    user = await auth_service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user


class RequirePermission:

    def __init__(self, permission: Permission):
        self.permission = permission

    async def __call__(
        self, current_user: Annotated[User, Depends(require_auth)]
    ) -> User:
        if not user_has_permission(current_user.role, self.permission):
            raise AuthorizationError(
                f"Permission denied: {self.permission.value} required"
            )
        return current_user


class RequireAnyPermission:

    def __init__(self, *permissions: Permission):
        self.permissions = permissions

    async def __call__(
        self, current_user: Annotated[User, Depends(require_auth)]
    ) -> User:
        if not any(
            user_has_permission(current_user.role, perm) for perm in self.permissions
        ):
            perms_str = ", ".join([p.value for p in self.permissions])
            raise AuthorizationError(
                f"Permission denied: one of [{perms_str}] required"
            )
        return current_user


class RequireAllPermissions:

    def __init__(self, *permissions: Permission):
        self.permissions = permissions

    async def __call__(
        self, current_user: Annotated[User, Depends(require_auth)]
    ) -> User:
        if not all(
            user_has_permission(current_user.role, perm) for perm in self.permissions
        ):
            perms_str = ", ".join([p.value for p in self.permissions])
            raise AuthorizationError(
                f"Permission denied: all of [{perms_str}] required"
            )
        return current_user
