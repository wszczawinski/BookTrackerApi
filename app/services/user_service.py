import logging
from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.exceptions import NotFoundError, ValidationError
from app.models.domain.user import User
from app.models.requests.user_requests import UserUpdate

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: UUID) -> User:
        user = await self.session.get(User, user_id)
        if not user:
            raise NotFoundError("User", str(user_id))
        return user

    async def get_all_users(
        self, skip: int = 0, limit: int = 100, active_only: bool = True
    ) -> Sequence[User]:
        statement = select(User).offset(skip).limit(limit)

        if active_only:
            statement = statement.where(User.is_active)

        result = await self.session.execute(statement)
        return result.scalars().all()

    async def update_user(self, user_id: UUID, user_update: UserUpdate) -> User:
        user = await self.session.get(User, user_id)
        if not user:
            raise NotFoundError("User", str(user_id))

        update_data = user_update.model_dump(exclude_unset=True)
        
        if not update_data:
            raise ValidationError("No fields provided for update")
        
        for key, value in update_data.items():
            setattr(user, key, value)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        
        logger.info(f"Updated user {user_id}")
        return user
