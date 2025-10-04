from sqlmodel import Field, SQLModel
from pydantic import EmailStr, StringConstraints
from typing import Optional, Annotated


class UserCreate(SQLModel):
    github_id: int = Field(unique=True, index=True)
    username: Annotated[str, StringConstraints(min_length=1, max_length=39)] = Field(
        index=True
    )
    email: EmailStr = Field(index=True)
    avatar_url: Optional[Annotated[str, StringConstraints(max_length=500)]] = Field(
        default=None
    )
    display_name: Optional[Annotated[str, StringConstraints(max_length=100)]] = Field(
        default=None
    )


class UserUpdate(SQLModel):
    display_name: Optional[Annotated[str, StringConstraints(max_length=100)]] = Field(
        default=None
    )
    avatar_url: Optional[Annotated[str, StringConstraints(max_length=500)]] = Field(
        default=None
    )
    is_active: Optional[bool] = Field(default=None)
