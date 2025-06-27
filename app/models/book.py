from sqlmodel import Field, SQLModel
from pydantic import field_validator, StringConstraints
from typing import Optional, Annotated

from .base import BaseModel


class BookBase(SQLModel):
    title: Annotated[str, StringConstraints(min_length=1, max_length=200)] = Field(index=True)
    author: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    isbn: Optional[Annotated[str, StringConstraints(pattern=r'^(?:\d{10}|\d{13})$')]] = Field(default=None)
    olid: Optional[Annotated[str, StringConstraints(pattern=r'^OL[0-9M]+[A-Z]$')]] = Field(default=None)
    cover_url: Optional[Annotated[str, StringConstraints(max_length=500)]] = Field(default=None)
    openlibrary_url: Optional[Annotated[str, StringConstraints(max_length=500)]] = Field(default=None)

    @field_validator('cover_url', 'openlibrary_url')
    def validate_urls(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return value


class Book(BookBase, BaseModel, table=True):
    pass


class BookCreate(BookBase):
    pass
