from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_utils.cbv import cbv
from typing import List, Optional
from uuid import UUID

from app.models.responses.book_responses import BookPublic
from app.models.requests.book_requests import BookCreate, BookUpdate
from app.services.book_service import BookService
from app.services.dependencies import get_book_service

router = APIRouter()


@cbv(router)
class BookController:
    book_service: BookService = Depends(get_book_service)

    @router.post("/", response_model=BookPublic, status_code=201)
    def create_book(self, book: BookCreate):
        try:
            created_book = self.book_service.create_book(book)
            return BookPublic.model_validate(created_book)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/", response_model=List[BookPublic])
    def get_books(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        search: Optional[str] = Query(None),
    ):
        if search:
            books = self.book_service.search_books(search)
        else:
            books = self.book_service.get_all_books(skip=skip, limit=limit)
        return [BookPublic.model_validate(book) for book in books]

    @router.get("/{book_id}", response_model=BookPublic)
    def get_book(self, book_id: UUID):
        book = self.book_service.get_book_by_id(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return BookPublic.model_validate(book)

    @router.put("/{book_id}", response_model=BookPublic)
    def update_book(self, book_id: UUID, book_update: BookUpdate):
        book = self.book_service.update_book(book_id, book_update)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return BookPublic.model_validate(book)

    @router.delete("/{book_id}", status_code=204)
    def delete_book(self, book_id: UUID):
        success = self.book_service.delete_book(book_id)
        if not success:
            raise HTTPException(status_code=404, detail="Book not found")
