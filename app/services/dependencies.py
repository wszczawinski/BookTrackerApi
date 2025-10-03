from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_session
from app.services.book_service import BookService
from app.services.reading_entry_service import ReadingEntryService
from app.services.user_service import UserService


def get_book_service(session: Session = Depends(get_session)) -> BookService:
    '''Dependency to get BookService instance.'''
    return BookService(session)


def get_reading_entry_service(session: Session = Depends(get_session)) -> ReadingEntryService:
    '''Dependency to get ReadingEntryService instance.'''
    return ReadingEntryService(session)


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    '''Dependency to get UserService instance.'''
    return UserService(session)
