from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.auth import RequirePermission
from app.core.permissions import Permission
from app.models.domain.user import User
from app.models.requests.book_requests import BookCreate, BookUpdate
from app.models.responses.book_responses import BookPublic
from app.services.book_service import BookService
from app.services.dependencies import get_book_service

router = APIRouter()


@router.post("/", response_model=BookPublic, status_code=201)
async def create_book(
    book: BookCreate,
    authenticated_user: User = Depends(RequirePermission(Permission.CREATE_BOOK)),
    book_service: BookService = Depends(get_book_service),
):
    try:
        created_book = await book_service.create_book(book)
        return BookPublic.model_validate(created_book)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[BookPublic])
async def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    authenticated_user: User = Depends(RequirePermission(Permission.VIEW_BOOK)),
    book_service: BookService = Depends(get_book_service),
):
    if search:
        books = await book_service.search_books(search)
    else:
        books = await book_service.get_all_books(skip=skip, limit=limit)
    return [BookPublic.model_validate(book) for book in books]


@router.get("/{book_id}", response_model=BookPublic)
async def get_book(
    book_id: UUID,
    authenticated_user: User = Depends(RequirePermission(Permission.VIEW_BOOK)),
    book_service: BookService = Depends(get_book_service),
):
    book = await book_service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookPublic.model_validate(book)


@router.put("/{book_id}", response_model=BookPublic)
async def update_book(
    book_id: UUID,
    book_update: BookUpdate,
    authenticated_user: User = Depends(RequirePermission(Permission.EDIT_BOOK)),
    book_service: BookService = Depends(get_book_service),
):
    book = await book_service.update_book(book_id, book_update)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookPublic.model_validate(book)


@router.delete("/{book_id}", status_code=204)
async def delete_book(
    book_id: UUID,
    authenticated_user: User = Depends(RequirePermission(Permission.DELETE_BOOK)),
    book_service: BookService = Depends(get_book_service),
):
    success = await book_service.delete_book(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
