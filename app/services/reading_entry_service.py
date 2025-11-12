import logging
from decimal import Decimal
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.exceptions import NotFoundError
from app.models.domain.book import Book
from app.models.domain.reading_entry import ReadingEntry, ReadingStatus
from app.models.domain.user import User

logger = logging.getLogger(__name__)


class ReadingEntryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_entry_by_id(self, entry_id: UUID) -> ReadingEntry:
        entry = await self.session.get(ReadingEntry, entry_id)
        if not entry:
            raise NotFoundError("Reading entry", str(entry_id))
        return entry

    async def get_user_entries(
        self, user_id: UUID, status: Optional[ReadingStatus] = None
    ) -> Sequence[ReadingEntry]:
        statement = select(ReadingEntry).where(ReadingEntry.user_id == user_id)

        if status:
            statement = statement.where(ReadingEntry.status == status)

        result = await self.session.execute(statement)
        return result.scalars().all()

    async def add_book_to_library(self, user_id: UUID, book_id: UUID) -> ReadingEntry:
        user = await self.session.get(User, user_id)
        if not user:
            raise NotFoundError("User", str(user_id))

        book = await self.session.get(Book, book_id)
        if not book:
            raise NotFoundError("Book", str(book_id))

        result = await self.session.execute(
            select(ReadingEntry).where(
                ReadingEntry.user_id == user_id,
                ReadingEntry.book_id == book_id,
            )
        )
        existing_entry = result.scalars().first()

        if existing_entry:
            logger.info(f"Book {book_id} already in library for user {user_id}")
            return existing_entry

        entry = ReadingEntry(
            user_id=user_id, book_id=book_id, status=ReadingStatus.WANT_TO_READ
        )

        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)

        logger.info(f"Added book {book_id} to library for user {user_id}")
        return entry

    async def start_reading(self, entry_id: UUID) -> ReadingEntry:
        entry = await self.session.get(ReadingEntry, entry_id)
        if not entry:
            raise NotFoundError("Reading entry", str(entry_id))

        entry.start_reading()
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)

        logger.info(f"Started reading entry {entry_id}")
        return entry

    async def update_reading_progress(
        self, entry_id: UUID, progress: Decimal
    ) -> ReadingEntry:
        entry = await self.session.get(ReadingEntry, entry_id)
        if not entry:
            raise NotFoundError("Reading entry", str(entry_id))

        entry.update_progress(progress)
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)

        logger.info(f"Updated progress for entry {entry_id} to {progress}%")
        return entry

    async def complete_reading(self, entry_id: UUID) -> ReadingEntry:
        entry = await self.session.get(ReadingEntry, entry_id)
        if not entry:
            raise NotFoundError("Reading entry", str(entry_id))

        entry.mark_completed()
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)

        logger.info(f"Completed reading entry {entry_id}")
        return entry

    async def abandon_reading(self, entry_id: UUID) -> ReadingEntry:
        entry = await self.session.get(ReadingEntry, entry_id)
        if not entry:
            raise NotFoundError("Reading entry", str(entry_id))

        entry.mark_abandoned()
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)

        logger.info(f"Abandoned reading entry {entry_id}")
        return entry

    async def update_review(
        self, entry_id: UUID, rating: int, review: Optional[str] = None
    ) -> ReadingEntry:
        entry = await self.session.get(ReadingEntry, entry_id)
        if not entry:
            raise NotFoundError("Reading entry", str(entry_id))

        entry.rating = rating
        entry.review = review

        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)

        logger.info(f"Updated review for entry {entry_id}")
        return entry

    async def delete_entry(self, entry_id: UUID) -> None:
        entry = await self.session.get(ReadingEntry, entry_id)
        if not entry:
            raise NotFoundError("Reading entry", str(entry_id))

        await self.session.delete(entry)
        await self.session.commit()

        logger.info(f"Deleted reading entry {entry_id}")
        return None
