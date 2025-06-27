from fastapi import APIRouter

from app.core.api import APIRoutes
from .controllers import books, reading_entries

api_router = APIRouter()

api_router.include_router(
    books.router,
    prefix=APIRoutes.BOOKS.prefix,
    tags=APIRoutes.BOOKS.tags,
)

api_router.include_router(
    reading_entries.router,
    prefix=APIRoutes.READING_ENTRIES.prefix,
    tags=APIRoutes.READING_ENTRIES.tags
)
