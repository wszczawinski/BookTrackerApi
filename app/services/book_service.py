from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.domain.book import Book
from app.models.requests.book_requests import BookCreate, BookUpdate


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_book(self, book_data: BookCreate) -> Book:
        book = Book.model_validate(book_data)
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def get_book_by_id(self, book_id: UUID) -> Optional[Book]:
        return await self.session.get(Book, book_id)

    async def get_all_books(self, skip: int = 0, limit: int = 100) -> Sequence[Book]:
        statement = select(Book).offset(skip).limit(limit)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def update_book(
        self, book_id: UUID, book_update: BookUpdate
    ) -> Optional[Book]:
        book = await self.session.get(Book, book_id)
        if not book:
            return None

        update_data = book_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(book, key, value)

        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def delete_book(self, book_id: UUID) -> bool:
        book = await self.session.get(Book, book_id)
        if not book:
            return False

        await self.session.delete(book)
        await self.session.commit()
        return True

    async def search_books(self, query: str) -> Sequence[Book]:
        statement = select(Book).where(
            (Book.title.ilike(f"%{query}%")) | (Book.author.ilike(f"%{query}%"))
        )
        result = await self.session.execute(statement)
        return result.scalars().all()
