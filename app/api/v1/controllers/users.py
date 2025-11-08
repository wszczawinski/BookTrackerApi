from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.auth import RequirePermission
from app.core.permissions import Permission
from app.models.domain.user import User
from app.models.responses.user_responses import UserPublic
from app.services.dependencies import get_user_service
from app.services.user_service import UserService

router = APIRouter()


@router.get("/", response_model=List[UserPublic])
async def get_users(
    authenticated_user: User = Depends(RequirePermission(Permission.VIEW_ALL_USERS)),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = Query(True),
    user_service: UserService = Depends(get_user_service),
):
    users = await user_service.get_all_users(
        skip=skip, limit=limit, active_only=active_only
    )
    return [UserPublic.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserPublic)
async def get_user(
    user_id: UUID,
    authenticated_user: User = Depends(RequirePermission(Permission.VIEW_USER_PROFILE)),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserPublic.model_validate(user)
