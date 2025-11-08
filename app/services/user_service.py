from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.domain.user import User
from app.models.requests.user_requests import UserUpdate


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return await self.session.get(User, user_id)

    async def get_all_users(
        self, skip: int = 0, limit: int = 100, active_only: bool = True
    ) -> Sequence[User]:
        statement = select(User).offset(skip).limit(limit)

        if active_only:
            statement = statement.where(User.is_active)

        result = await self.session.execute(statement)
        return result.scalars().all()

    async def update_user(
        self, user_id: UUID, user_update: UserUpdate
    ) -> Optional[User]:
        user = await self.session.get(User, user_id)
        if not user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def deactivate_user(self, user_id: UUID) -> bool:
        user = await self.session.get(User, user_id)
        if not user:
            return False

        user.is_active = False
        self.session.add(user)
        await self.session.commit()
        return True

    async def reactivate_user(self, user_id: UUID) -> bool:
        user = await self.session.get(User, user_id)
        if not user:
            return False

        user.is_active = True
        self.session.add(user)
        await self.session.commit()
        return True
