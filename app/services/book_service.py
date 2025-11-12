import logging
from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.exceptions import NotFoundError, ValidationError
from app.models.domain.book import Book
from app.models.requests.book_requests import BookCreate, BookUpdate

logger = logging.getLogger(__name__)


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_book(self, book_data: BookCreate) -> Book:
        book = Book.model_validate(book_data)

        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)

        logger.info(f"Created book {book.id}: {book.title}")
        return book

    async def get_book_by_id(self, book_id: UUID) -> Book:
        book = await self.session.get(Book, book_id)
        if not book:
            raise NotFoundError("Book", str(book_id))

        return book

    async def get_all_books(self, skip: int = 0, limit: int = 100) -> Sequence[Book]:
        statement = select(Book).offset(skip).limit(limit)
        result = await self.session.execute(statement)

        return result.scalars().all()

    async def update_book(self, book_id: UUID, book_update: BookUpdate) -> Book:
        book = await self.session.get(Book, book_id)
        if not book:
            raise NotFoundError("Book", str(book_id))

        update_data = book_update.model_dump(exclude_unset=True)

        if not update_data:
            raise ValidationError("No fields provided for update")

        for key, value in update_data.items():
            setattr(book, key, value)

        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)

        logger.info(f"Updated book {book_id}")
        return book

    async def delete_book(self, book_id: UUID) -> None:
        book = await self.session.get(Book, book_id)
        if not book:
            raise NotFoundError("Book", str(book_id))

        await self.session.delete(book)
        await self.session.commit()

        logger.info(f"Deleted book {book_id}")
        return None

    async def search_books(self, query: str) -> Sequence[Book]:
        statement = select(Book).where(
            (Book.title.ilike(f"%{query}%")) | (Book.author.ilike(f"%{query}%"))
        )
        result = await self.session.execute(statement)
        return result.scalars().all()
