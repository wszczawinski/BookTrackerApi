from uuid import UUID
from typing import List, Optional
from decimal import Decimal
from sqlmodel import Session, select

from app.models.reading_entry import (
    ReadingEntry,
    ReadingEntryCreate,
    ReadingStatus,
)
from app.models.user import User
from app.models.book import Book


class ReadingEntryService:

    def __init__(self, session: Session):
        self.session = session

    def get_entry_by_id(self, entry_id: UUID) -> Optional[ReadingEntry]:
        return self.session.get(ReadingEntry, entry_id)

    def get_user_entries(
        self, user_id: UUID, status: Optional[ReadingStatus] = None
    ) -> List[ReadingEntry]:
        statement = select(ReadingEntry).where(ReadingEntry.user_id == user_id)

        if status:
            statement = statement.where(ReadingEntry.status == status)

        return self.session.exec(statement).all()

    def add_book_to_wishlist(self, user_id: UUID, book_id: UUID) -> ReadingEntry:
        user = self.session.get(User, user_id)
        if not user:
            raise ValueError("User not found")

        book = self.session.get(Book, book_id)
        if not book:
            raise ValueError("Book not found")

        existing_entry = self.session.exec(
            select(ReadingEntry).where(
                ReadingEntry.user_id == user_id,
                ReadingEntry.book_id == book_id,
            )
        ).first()

        if existing_entry:
            return existing_entry

        entry = ReadingEntry(
            user_id=user_id, book_id=book_id, status=ReadingStatus.WANT_TO_READ
        )

        self.session.add(entry)
        self.session.commit()
        self.session.refresh(entry)
        return entry

    def start_reading(self, entry_id: UUID) -> Optional[ReadingEntry]:
        entry = self.session.get(ReadingEntry, entry_id)
        if not entry:
            return None

        entry.start_reading()
        self.session.add(entry)
        self.session.commit()
        self.session.refresh(entry)
        return entry

    def update_reading_progress(
        self, entry_id: UUID, progress: Decimal
    ) -> Optional[ReadingEntry]:
        entry = self.session.get(ReadingEntry, entry_id)
        if not entry:
            return None

        entry.update_progress(progress)
        self.session.add(entry)
        self.session.commit()
        self.session.refresh(entry)
        return entry

    def complete_reading(self, entry_id: UUID) -> Optional[ReadingEntry]:
        entry = self.session.get(ReadingEntry, entry_id)
        if not entry:
            return None

        entry.mark_completed()
        self.session.add(entry)
        self.session.commit()
        self.session.refresh(entry)
        return entry

    def abandon_reading(self, entry_id: UUID) -> Optional[ReadingEntry]:
        entry = self.session.get(ReadingEntry, entry_id)
        if not entry:
            return None

        entry.mark_abandoned()
        self.session.add(entry)
        self.session.commit()
        self.session.refresh(entry)
        return entry

    def update_review(
        self, entry_id: UUID, rating: int, review: Optional[str] = None
    ) -> Optional[ReadingEntry]:
        entry = self.session.get(ReadingEntry, entry_id)
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
        self.session.commit()
        self.session.refresh(entry)
        return entry

    def delete_entry(self, entry_id: UUID) -> bool:
        entry = self.session.get(ReadingEntry, entry_id)
        if not entry:
            return False

        self.session.delete(entry)
        self.session.commit()
        return True
