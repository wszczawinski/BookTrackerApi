from sqlmodel import Field, SQLModel

from pydantic import StringConstraints, model_validator
from datetime import datetime
from decimal import Decimal
from typing import Optional, Annotated
from uuid import UUID
from enum import Enum

from .base import BaseModel


class ReadingStatus(str, Enum):
    WANT_TO_READ = "want_to_read"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class ReadingEntryBase(SQLModel):
    book_id: UUID = Field(foreign_key="book.id")
    start_date: Optional[datetime] = Field(default=None, index=True)
    end_date: Optional[datetime] = Field(default=None)
    progress: Annotated[Decimal, Field(ge=0, le=100)] = Field(default=0)
    rating: Optional[Annotated[int, Field(ge=1, le=5)]] = Field(default=None)
    review: Optional[Annotated[str, StringConstraints(max_length=2000)]] = Field(default=None)
    status: ReadingStatus = Field(
        default=ReadingStatus.WANT_TO_READ,
        index=True,
        description="Current reading status"
    )

    @model_validator(mode='after')
    def validate_dates_and_status(self) -> 'ReadingEntryBase':
        if self.end_date and self.start_date:
            if self.end_date < self.start_date:
                raise ValueError('end_date cannot be earlier than start_date')

        if self.status == ReadingStatus.COMPLETED:
            if self.progress != 100:
                raise ValueError('progress must be 100 when status is COMPLETED')
            if not self.end_date:
                raise ValueError('end_date is required when status is COMPLETED')

        if self.status == ReadingStatus.IN_PROGRESS and not self.start_date:
            raise ValueError('start_date is required when status is IN_PROGRESS')

        return self


class ReadingEntryCreate(ReadingEntryBase):
    pass


class ReadingEntryUpdate(SQLModel):
    start_date: Optional[datetime] = Field(default=None)
    end_date: Optional[datetime] = Field(default=None)
    progress: Optional[Annotated[Decimal, Field(ge=0, le=100)]] = Field(default=None)
    rating: Optional[Annotated[int, Field(ge=1, le=5)]] = Field(default=None)
    review: Optional[Annotated[str, StringConstraints(max_length=2000)]] = Field(default=None)
    status: Optional[ReadingStatus] = Field(default=None)

    @model_validator(mode='after')
    def validate_partial_update(self) -> 'ReadingEntryUpdate':
        if self.status == ReadingStatus.COMPLETED:
            if self.progress is not None and self.progress != 100:
                raise ValueError('progress must be 100 when status is COMPLETED')

        if self.end_date and self.start_date:
            if self.end_date < self.start_date:
                raise ValueError('end_date cannot be earlier than start_date')

        return self


class ReadingEntry(ReadingEntryBase, BaseModel, table=True):
    pass
