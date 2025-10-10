from fastapi import Depends, HTTPException, status, Request
from sqlmodel import Session

from app.core.config import settings
from app.core.database import get_session
from app.services.book_service import BookService
from app.services.reading_entry_service import ReadingEntryService
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.models.domain.user import User


def get_book_service(session: Session = Depends(get_session)) -> BookService:
    """Dependency to get BookService instance."""
    return BookService(session)


def get_reading_entry_service(
    session: Session = Depends(get_session),
) -> ReadingEntryService:
    """Dependency to get ReadingEntryService instance."""
    return ReadingEntryService(session)


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    """Dependency to get UserService instance."""
    return UserService(session)


def get_auth_service(session: Session = Depends(get_session)) -> AuthService:
    """Dependency to get AuthService instance."""
    return AuthService(session)


def require_auth(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    """Dependency that requires authentication via HTTP-only cookie."""
    token = request.cookies.get(settings.API_JWT_COOKIE_NAME)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required - please login",
        )

    user = auth_service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user
