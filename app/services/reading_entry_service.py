from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.domain.book import Book
from app.models.domain.reading_entry import ReadingEntry, ReadingStatus
from app.models.domain.user import User


class ReadingEntryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_entry_by_id(self, entry_id: UUID) -> Optional[ReadingEntry]:
        return await self.session.get(ReadingEntry, entry_id)

    async def get_user_entries(
        self, user_id: UUID, status: Optional[ReadingStatus] = None
    ) -> List[ReadingEntry]:
        statement = select(ReadingEntry).where(ReadingEntry.user_id == user_id)

        if status:
            statement = statement.where(ReadingEntry.status == status)

        result = await self.session.execute(statement)
        return result.scalars().all()

    async def add_book_to_library(self, user_id: UUID, book_id: UUID) -> ReadingEntry:
        user = await self.session.get(User, user_id)
        if not user:
            raise ValueError("User not found")

        book = await self.session.get(Book, book_id)
        if not book:
            raise ValueError("Book not found")

        result = await self.session.execute(
            select(ReadingEntry).where(
                ReadingEntry.user_id == user_id,
                ReadingEntry.book_id == book_id,
            )
        )
        existing_entry = result.scalars().first()

        if existing_entry:
            return existing_entry

        entry = ReadingEntry(
            user_id=user_id, book_id=book_id, status=ReadingStatus.WANT_TO_READ
        )

        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)
        return entry

    async def start_reading(self, entry_id: UUID) -> Optional[ReadingEntry]:
        entry = await self.session.get(ReadingEntry, entry_id)
        if not entry:
            return None

        entry.start_reading()
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)
        return entry

    async def update_reading_progress(
        self, entry_id: UUID, progress: Decimal
    ) -> Optional[ReadingEntry]:
        entry = await self.session.get(ReadingEntry, entry_id)
        if not entry:
            return None

        entry.update_progress(progress)
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)
        return entry

    async def complete_reading(self, entry_id: UUID) -> Optional[ReadingEntry]:
        entry = await self.session.get(ReadingEntry, entry_id)
        if not entry:
            return None

        entry.mark_completed()
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)
        return entry

    async def abandon_reading(self, entry_id: UUID) -> Optional[ReadingEntry]:
        entry = await self.session.get(ReadingEntry, entry_id)
        if not entry:
            return None

        entry.mark_abandoned()
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)
        return entry

    async def update_review(
        self, entry_id: UUID, rating: int, review: Optional[str] = None
    ) -> Optional[ReadingEntry]:
        entry = await self.session.get(ReadingEntry, entry_id)
        if not entry:
            return None

        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        entry.rating = rating

        if review is not None:
            if len(review) > 2000:
                raise ValueError("Review must be 2000 characters or less")
            entry.review = review

        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)
        return entry

    async def delete_entry(self, entry_id: UUID) -> bool:
        entry = await self.session.get(ReadingEntry, entry_id)
        if not entry:
            return False

        await self.session.delete(entry)
        await self.session.commit()
        return True
