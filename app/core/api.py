from enum import StrEnum
from typing import NamedTuple


class APIRoutePrefix(StrEnum):
    BOOKS = "/books"
    READING_ENTRIES = "/reading-entries"


class APITags(StrEnum):
    BOOKS = "books"
    READING_ENTRIES = "reading_entries"


class APIRoute(NamedTuple):
    prefix: str
    tags: list[str]
    description: str = ""


class APIRoutes:
    BOOKS = APIRoute(
        prefix=APIRoutePrefix.BOOKS,
        tags=[APITags.BOOKS],
        description="Operations with books"
    )
    READING_ENTRIES = APIRoute(
        prefix=APIRoutePrefix.READING_ENTRIES,
        tags=[APITags.READING_ENTRIES],
        description="Operations with reading entries"
    )


api_metadata = {
    "tags": [
        {
            "name": APITags.BOOKS,
            "description": "Manage books in the library"
        },
        {
            "name": APITags.READING_ENTRIES,
            "description": "Manage reading progress and reviews"
        }
    ]
}
