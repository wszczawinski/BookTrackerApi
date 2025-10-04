from .user_requests import UserCreate, UserUpdate
from .book_requests import BookCreate, BookUpdate
from .reading_entry_requests import (
    AddBookRequest,
    UpdateProgressRequest,
    UpdateReviewRequest,
)

__all__ = [
    "UserCreate",
    "UserUpdate",
    "BookCreate", 
    "BookUpdate",
    "AddBookRequest",
    "UpdateProgressRequest",
    "UpdateReviewRequest",
]
