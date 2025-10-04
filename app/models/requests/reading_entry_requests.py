from sqlmodel import Field, SQLModel
from pydantic import StringConstraints, BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional, Annotated
from uuid import UUID

from ..domain.reading_entry import ReadingStatus


class AddBookRequest(BaseModel):
    user_id: UUID
    book_id: UUID


class UpdateProgressRequest(BaseModel):
    progress: Decimal


class UpdateReviewRequest(BaseModel):
    rating: int
    review: Optional[str] = None


class ReadingEntryUpdate(SQLModel):
    start_date: Optional[datetime] = Field(default=None)
    end_date: Optional[datetime] = Field(default=None)
    progress: Optional[Annotated[Decimal, Field(ge=0, le=100)]] = Field(default=None)
    rating: Optional[Annotated[int, Field(ge=1, le=5)]] = Field(default=None)
    review: Optional[Annotated[str, StringConstraints(max_length=2000)]] = Field(default=None)
    status: Optional[ReadingStatus] = Field(default=None)