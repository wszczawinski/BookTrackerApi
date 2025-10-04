from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select

from app.models.domain.book import Book
from app.models.requests.book_requests import BookCreate, BookUpdate


class BookService:

    def __init__(self, session: Session):
        self.session = session

    def create_book(self, book_data: BookCreate) -> Book:
        book = Book.model_validate(book_data)
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book

    def get_book_by_id(self, book_id: UUID) -> Optional[Book]:
        return self.session.get(Book, book_id)

    def get_all_books(self, skip: int = 0, limit: int = 100) -> List[Book]:
        statement = select(Book).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update_book(self, book_id: UUID, book_update: BookUpdate) -> Optional[Book]:
        book = self.session.get(Book, book_id)
        if not book:
            return None

        update_data = book_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(book, key, value)

        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book

    def delete_book(self, book_id: UUID) -> bool:
        book = self.session.get(Book, book_id)
        if not book:
            return False

        self.session.delete(book)
        self.session.commit()
        return True

    def search_books(self, query: str) -> List[Book]:
        statement = select(Book).where(
            (Book.title.ilike(f'%{query}%')) | (Book.author.ilike(f'%{query}%'))
        )
        return self.session.exec(statement).all()
