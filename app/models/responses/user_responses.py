from sqlmodel import SQLModel
from typing import Optional
from uuid import UUID


class UserPublic(SQLModel):
    id: UUID
    username: str
    display_name: Optional[str]
    avatar_url: Optional[str]
