from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, StringConstraints
from sqlmodel import Field, SQLModel

from ..domain.reading_entry import ReadingStatus


class AddBookRequest(BaseModel):
    user_id: UUID
    book_id: UUID


class UpdateProgressRequest(BaseModel):
    progress: Annotated[Decimal, Field(ge=0, le=100)]


class UpdateReviewRequest(BaseModel):
    rating: Annotated[int, Field(ge=1, le=5)]
    review: Optional[Annotated[str, StringConstraints(max_length=2000)]] = None


class ReadingEntryUpdate(SQLModel):
    start_date: Optional[datetime] = Field(default=None)
    end_date: Optional[datetime] = Field(default=None)
    progress: Optional[Annotated[Decimal, Field(ge=0, le=100)]] = Field(default=None)
    rating: Optional[Annotated[int, Field(ge=1, le=5)]] = Field(default=None)
    review: Optional[Annotated[str, StringConstraints(max_length=2000)]] = Field(
        default=None
    )
    status: Optional[ReadingStatus] = Field(default=None)
