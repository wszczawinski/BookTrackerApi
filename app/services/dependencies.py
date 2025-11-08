from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.services.auth_service import AuthService
from app.services.book_service import BookService
from app.services.reading_entry_service import ReadingEntryService
from app.services.user_service import UserService


def get_book_service(session: AsyncSession = Depends(get_session)) -> BookService:
    """Dependency to get BookService instance."""
    return BookService(session)


def get_reading_entry_service(
    session: AsyncSession = Depends(get_session),
) -> ReadingEntryService:
    """Dependency to get ReadingEntryService instance."""
    return ReadingEntryService(session)


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    """Dependency to get UserService instance."""
    return UserService(session)


def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    """Dependency to get AuthService instance."""
    return AuthService(session)
