from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_utils.cbv import cbv
from pydantic import BaseModel

from app.models.reading_entry import ReadingEntry, ReadingEntryPublic, ReadingStatus
from app.services.reading_entry_service import ReadingEntryService
from app.services.dependencies import get_reading_entry_service

router = APIRouter()


class AddBookRequest(BaseModel):
    user_id: UUID
    book_id: UUID


class UpdateProgressRequest(BaseModel):
    progress: Decimal


class UpdateReviewRequest(BaseModel):
    rating: int
    review: Optional[str] = None


@cbv(router)
class ReadingEntryController:
    service: ReadingEntryService = Depends(get_reading_entry_service)

    @router.get("/", response_model=List[ReadingEntryPublic])
    def get_reading_entries(
        self,
        user_id: UUID = Query(..., description="User ID to get entries for"),
        status: Optional[ReadingStatus] = Query(
            None, description="Filter by reading status"
        ),
    ):
        """Get reading entries for a user, optionally filtered by status."""
        entries = self.service.get_user_entries(user_id, status)
        return [ReadingEntryPublic.model_validate(entry) for entry in entries]

    @router.get("/{entry_id}", response_model=ReadingEntryPublic)
    def get_reading_entry(self, entry_id: UUID):
        entry = self.service.get_entry_by_id(entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Reading entry not found")
        return ReadingEntryPublic.model_validate(entry)

    @router.post("/library", response_model=ReadingEntryPublic, status_code=201)
    def add_book_to_wishlist(self, request: AddBookRequest):
        try:
            entry = self.service.add_book_to_wishlist(request.user_id, request.book_id)
            return ReadingEntryPublic.model_validate(entry)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.patch("/{entry_id}/start-reading", response_model=ReadingEntryPublic)
    def start_reading(self, entry_id: UUID):
        try:
            entry = self.service.start_reading(entry_id)
            if not entry:
                raise HTTPException(status_code=404, detail="Reading entry not found")
            return ReadingEntryPublic.model_validate(entry)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.patch("/{entry_id}/progress", response_model=ReadingEntryPublic)
    def update_progress(self, entry_id: UUID, request: UpdateProgressRequest):
        try:
            entry = self.service.update_reading_progress(entry_id, request.progress)
            if not entry:
                raise HTTPException(status_code=404, detail="Reading entry not found")
            return ReadingEntryPublic.model_validate(entry)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.patch("/{entry_id}/review", response_model=ReadingEntryPublic)
    def update_review(self, entry_id: UUID, request: UpdateReviewRequest):
        try:
            entry = self.service.update_review(entry_id, request.rating, request.review)
            if not entry:
                raise HTTPException(status_code=404, detail="Reading entry not found")
            return ReadingEntryPublic.model_validate(entry)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.patch("/{entry_id}/complete", response_model=ReadingEntryPublic)
    def complete_reading(self, entry_id: UUID):
        entry = self.service.complete_reading(entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Reading entry not found")
        return ReadingEntryPublic.model_validate(entry)

    @router.patch("/{entry_id}/abandon", response_model=ReadingEntryPublic)
    def abandon_reading(self, entry_id: UUID):
        entry = self.service.abandon_reading(entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Reading entry not found")
        return ReadingEntryPublic.model_validate(entry)

    @router.delete("/{entry_id}", status_code=204)
    def delete_reading_entry(self, entry_id: UUID):
        success = self.service.delete_entry(entry_id)
        if not success:
            raise HTTPException(status_code=404, detail="Reading entry not found")
