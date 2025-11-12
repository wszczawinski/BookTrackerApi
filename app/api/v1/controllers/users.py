from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.auth import RequirePermission, require_auth
from app.core.exceptions import NotFoundError, ValidationError
from app.core.permissions import Permission
from app.models.domain.user import User
from app.models.requests.user_requests import UserUpdate
from app.models.responses.user_responses import UserPublic
from app.services.dependencies import get_user_service
from app.services.user_service import UserService

router = APIRouter()


@router.get("/", response_model=List[UserPublic], operation_id="getUsers")
async def get_users(
    authenticated_user: Annotated[
        User, Depends(RequirePermission(Permission.VIEW_ALL_USERS))
    ],
    user_service: Annotated[UserService, Depends(get_user_service)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = Query(True),
) -> List[UserPublic]:
    users = await user_service.get_all_users(
        skip=skip, limit=limit, active_only=active_only
    )
    return [UserPublic.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserPublic, operation_id="getUser")
async def get_user(
    user_id: UUID,
    authenticated_user: Annotated[
        User, Depends(RequirePermission(Permission.VIEW_USER_PROFILE))
    ],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserPublic:
    try:
        user = await user_service.get_user_by_id(user_id)
        return UserPublic.model_validate(user)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/me", response_model=UserPublic, operation_id="updateOwnProfile")
async def update_own_profile(
    user_update: UserUpdate,
    authenticated_user: Annotated[User, Depends(require_auth)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserPublic:
    try:
        updated_user = await user_service.update_user(
            authenticated_user.id, user_update
        )
        return UserPublic.model_validate(updated_user)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
