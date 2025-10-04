from .base import BaseModel

# Domain models
from .domain.user import User
from .domain.book import Book
from .domain.reading_entry import ReadingEntry, ReadingStatus

# Request models
from .requests.user_requests import UserCreate, UserUpdate
from .requests.book_requests import BookCreate, BookUpdate
from .requests.reading_entry_requests import (
    AddBookRequest,
    UpdateProgressRequest,
    UpdateReviewRequest,
    ReadingEntryUpdate,
)

# Response models
from .responses.user_responses import UserPublic
from .responses.book_responses import BookPublic
from .responses.reading_entry_responses import ReadingEntryPublic

__all__ = [
    "BaseModel",
    # Domain models
    "User",
    "Book",
    "ReadingEntry",
    "ReadingStatus",
    # Request models
    "UserCreate",
    "UserUpdate",
    "BookCreate",
    "BookUpdate",
    "AddBookRequest",
    "UpdateProgressRequest",
    "UpdateReviewRequest",
    "ReadingEntryUpdate",
    # Response models
    "UserPublic",
    "BookPublic",
    "ReadingEntryPublic",
]
