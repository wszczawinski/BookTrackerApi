from enum import Enum
from typing import TYPE_CHECKING, Annotated, Optional

from pydantic import EmailStr, StringConstraints
from sqlmodel import Field, Relationship, SQLModel

from ..base import BaseModel

if TYPE_CHECKING:
    from .reading_entry import ReadingEntry


class RoleType(str, Enum):
    ADMIN = "admin"
    STANDARD_USER = "standard_user"


class UserBase(SQLModel):
    username: Annotated[str, StringConstraints(min_length=1, max_length=39)] = Field(
        index=True
    )
    email: EmailStr = Field(unique=True, index=True)
    avatar_url: Optional[Annotated[str, StringConstraints(max_length=500)]] = Field(
        default=None
    )
    display_name: Optional[Annotated[str, StringConstraints(max_length=100)]] = Field(
        default=None
    )
    is_active: bool = Field(default=True)
    role: RoleType = Field(default=RoleType.STANDARD_USER)


class User(UserBase, BaseModel, table=True):
    reading_entries: list["ReadingEntry"] = Relationship(back_populates="user")
