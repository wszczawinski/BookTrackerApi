from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_utils.cbv import cbv
from typing import List
from uuid import UUID

from app.models.user import User, UserCreate, UserPublic
from app.services.user_service import UserService
from app.services.dependencies import get_user_service

router = APIRouter()


@cbv(router)
class UserController:
    user_service: UserService = Depends(get_user_service)

    @router.post("/", response_model=UserPublic, status_code=201)
    def create_user(self, user: UserCreate):
        try:
            created_user = self.user_service.create_user(user)
            return UserPublic.model_validate(created_user)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/", response_model=List[UserPublic])
    def get_users(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        active_only: bool = Query(True),
    ):
        users = self.user_service.get_all_users(
            skip=skip, limit=limit, active_only=active_only
        )
        return [UserPublic.model_validate(user) for user in users]

    @router.get("/{user_id}", response_model=UserPublic)
    def get_user(self, user_id: UUID):
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserPublic.model_validate(user)
