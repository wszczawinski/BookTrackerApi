from uuid import UUID
from typing import List, Optional
from sqlmodel import Session, select

from app.models.user import User, UserCreate, UserUpdate


class UserService:

    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_data: UserCreate) -> User:
        existing_user = self.session.exec(
            select(User).where(User.github_id == user_data.github_id)
        ).first()

        if existing_user:
            raise ValueError('User with this GitHub ID already exists')

        user = User.model_validate(user_data)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return self.session.get(User, user_id)

    def get_all_users(
        self, skip: int = 0, limit: int = 100, active_only: bool = True
    ) -> List[User]:
        statement = select(User).offset(skip).limit(limit)

        if active_only:
            statement = statement.where(User.is_active == True)

        return self.session.exec(statement).all()

    def update_user(self, user_id: UUID, user_update: UserUpdate) -> Optional[User]:
        user = self.session.get(User, user_id)
        if not user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def deactivate_user(self, user_id: UUID) -> bool:
        user = self.session.get(User, user_id)
        if not user:
            return False

        user.is_active = False
        self.session.add(user)
        self.session.commit()
        return True

    def reactivate_user(self, user_id: UUID) -> bool:
        user = self.session.get(User, user_id)
        if not user:
            return False

        user.is_active = True
        self.session.add(user)
        self.session.commit()
        return True
