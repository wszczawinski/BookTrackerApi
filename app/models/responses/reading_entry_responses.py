from sqlmodel import SQLModel
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from ..domain.reading_entry import ReadingStatus


class ReadingEntryPublic(SQLModel):
    id: UUID
    book_id: UUID
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    progress: Decimal
    rating: Optional[int]
    review: Optional[str]
    status: ReadingStatus
    created_at: datetime
