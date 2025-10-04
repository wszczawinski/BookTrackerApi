from sqlmodel import Field, SQLModel, Relationship
from pydantic import StringConstraints, model_validator
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional, Annotated, TYPE_CHECKING
from uuid import UUID
from enum import Enum

from ..base import BaseModel

if TYPE_CHECKING:
    from .user import User
    from .book import Book


class ReadingStatus(str, Enum):
    WANT_TO_READ = "want_to_read"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class ReadingEntryBase(SQLModel):
    user_id: UUID = Field(foreign_key="user.id", index=True)
    book_id: UUID = Field(foreign_key="book.id")
    start_date: Optional[datetime] = Field(default=None, index=True)
    end_date: Optional[datetime] = Field(default=None)
    progress: Annotated[Decimal, Field(ge=0, le=100)] = Field(default=0)
    rating: Optional[Annotated[int, Field(ge=1, le=5)]] = Field(default=None)
    review: Optional[Annotated[str, StringConstraints(max_length=2000)]] = Field(default=None)
    status: ReadingStatus = Field(
        default=ReadingStatus.WANT_TO_READ,
        index=True,
        description="Current reading status",
    )

    @model_validator(mode="after")
    def validate_dates_and_status(self) -> "ReadingEntryBase":
        if self.end_date and self.start_date:
            if self.end_date < self.start_date:
                raise ValueError("end_date cannot be earlier than start_date")

        if self.status == ReadingStatus.COMPLETED:
            if self.progress != 100:
                raise ValueError("progress must be 100 when status is COMPLETED")
            if not self.end_date:
                raise ValueError("end_date is required when status is COMPLETED")

        if self.status == ReadingStatus.IN_PROGRESS and not self.start_date:
            raise ValueError("start_date is required when status is IN_PROGRESS")

        return self


class ReadingEntry(ReadingEntryBase, BaseModel, table=True):
    user: Optional["User"] = Relationship(back_populates="reading_entries")
    book: Optional["Book"] = Relationship(back_populates="reading_entries")

    def mark_completed(self, end_date: Optional[datetime] = None) -> None:
        if self.status == ReadingStatus.COMPLETED:
            return 

        self.status = ReadingStatus.COMPLETED
        self.progress = Decimal("100")
        self.end_date = end_date or datetime.now(timezone.utc)

        if not self.start_date:
            self.start_date = self.created_at

    def update_progress(self, percentage: Decimal) -> None:
        if not (0 <= percentage <= 100):
            raise ValueError("Progress must be between 0 and 100")

        self.progress = percentage

        if percentage == 0 and self.status != ReadingStatus.WANT_TO_READ:
            self.status = ReadingStatus.WANT_TO_READ
            self.start_date = None
        elif 0 < percentage < 100:
            self.status = ReadingStatus.IN_PROGRESS
            if not self.start_date:
                self.start_date = datetime.now(timezone.utc)
        elif percentage == 100:
            self.mark_completed()

    def mark_abandoned(self) -> None:
        self.status = ReadingStatus.ABANDONED

    def start_reading(self) -> None:
        from datetime import datetime, timezone

        if self.status != ReadingStatus.IN_PROGRESS:
            self.status = ReadingStatus.IN_PROGRESS
            if not self.start_date:
                self.start_date = datetime.now(timezone.utc)
