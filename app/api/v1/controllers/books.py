from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.auth import RequirePermission
from app.core.exceptions import NotFoundError, ValidationError
from app.core.permissions import Permission
from app.models.domain.user import User
from app.models.requests.book_requests import BookCreate, BookUpdate
from app.models.responses.book_responses import BookPublic
from app.services.book_service import BookService
from app.services.dependencies import get_book_service

router = APIRouter()


@router.post("/", response_model=BookPublic, status_code=201, operation_id="createBook")
async def create_book(
    book: BookCreate,
    authenticated_user: Annotated[
        User, Depends(RequirePermission(Permission.CREATE_BOOK))
    ],
    book_service: Annotated[BookService, Depends(get_book_service)],
) -> BookPublic:
    try:
        created_book = await book_service.create_book(book)
        return BookPublic.model_validate(created_book)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[BookPublic], operation_id="getBooks")
async def get_books(
    authenticated_user: Annotated[
        User, Depends(RequirePermission(Permission.VIEW_BOOK))
    ],
    book_service: Annotated[BookService, Depends(get_book_service)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
) -> List[BookPublic]:
    if search:
        books = await book_service.search_books(search)
    else:
        books = await book_service.get_all_books(skip=skip, limit=limit)
    return [BookPublic.model_validate(book) for book in books]


@router.get("/{book_id}", response_model=BookPublic, operation_id="getBook")
async def get_book(
    book_id: UUID,
    authenticated_user: Annotated[
        User, Depends(RequirePermission(Permission.VIEW_BOOK))
    ],
    book_service: Annotated[BookService, Depends(get_book_service)],
) -> BookPublic:
    try:
        book = await book_service.get_book_by_id(book_id)
        return BookPublic.model_validate(book)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{book_id}", response_model=BookPublic, operation_id="updateBook")
async def update_book(
    book_id: UUID,
    book_update: BookUpdate,
    authenticated_user: Annotated[
        User, Depends(RequirePermission(Permission.EDIT_BOOK))
    ],
    book_service: Annotated[BookService, Depends(get_book_service)],
) -> BookPublic:
    try:
        book = await book_service.update_book(book_id, book_update)
        return BookPublic.model_validate(book)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{book_id}", status_code=status.HTTP_204_NO_CONTENT, operation_id="deleteBook"
)
async def delete_book(
    book_id: UUID,
    authenticated_user: Annotated[
        User, Depends(RequirePermission(Permission.DELETE_BOOK))
    ],
    book_service: Annotated[BookService, Depends(get_book_service)],
) -> None:
    try:
        await book_service.delete_book(book_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
