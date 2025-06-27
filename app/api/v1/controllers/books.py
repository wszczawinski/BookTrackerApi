from sqlmodel import Session, select
from fastapi import APIRouter, Depends
from typing import List

from app.core.database import get_session
from app.models.book import Book, BookCreate

router = APIRouter()


@router.post("/", response_model=Book)
def create_book(book: BookCreate, session: Session = Depends(get_session)):
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@router.get("/", response_model=List[Book])
def get_books(session: Session = Depends(get_session)):
    return session.exec(select(Book)).all()
