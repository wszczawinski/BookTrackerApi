from sqlmodel import SQLModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class BookPublic(SQLModel):
    id: UUID
    title: str
    author: str
    isbn: Optional[str]
    olid: Optional[str]
    cover_url: Optional[str]
    openlibrary_url: Optional[str]
    created_at: datetime
