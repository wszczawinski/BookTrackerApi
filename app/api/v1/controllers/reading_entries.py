from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.auth import RequirePermission
from app.core.permissions import Permission
from app.models.domain.reading_entry import ReadingStatus
from app.models.domain.user import User
from app.models.requests.reading_entry_requests import (
    AddBookRequest,
    UpdateProgressRequest,
    UpdateReviewRequest,
)
from app.models.responses.reading_entry_responses import ReadingEntryPublic
from app.services.dependencies import get_reading_entry_service
from app.services.reading_entry_service import ReadingEntryService

router = APIRouter()


@router.get("/", response_model=List[ReadingEntryPublic])
async def get_reading_entries(
    user_id: UUID = Query(..., description="User ID to get entries for"),
    status: Optional[ReadingStatus] = Query(
        None, description="Filter by reading status"
    ),
    authenticated_user: User = Depends(
        RequirePermission(Permission.VIEW_OWN_READING_ENTRIES)
    ),
    service: ReadingEntryService = Depends(get_reading_entry_service),
):
    entries = await service.get_user_entries(user_id, status)
    return [ReadingEntryPublic.model_validate(entry) for entry in entries]


@router.get("/{entry_id}", response_model=ReadingEntryPublic)
async def get_reading_entry(
    entry_id: UUID,
    authenticated_user: User = Depends(
        RequirePermission(Permission.VIEW_READING_ENTRY)
    ),
    service: ReadingEntryService = Depends(get_reading_entry_service),
):
    entry = await service.get_entry_by_id(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Reading entry not found")
    return ReadingEntryPublic.model_validate(entry)


@router.post("/", response_model=ReadingEntryPublic, status_code=201)
async def add_book_to_library(
    request: AddBookRequest,
    authenticated_user: User = Depends(
        RequirePermission(Permission.CREATE_READING_ENTRY)
    ),
    service: ReadingEntryService = Depends(get_reading_entry_service),
):
    try:
        entry = await service.add_book_to_library(request.user_id, request.book_id)
        return ReadingEntryPublic.model_validate(entry)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{entry_id}/start-reading", response_model=ReadingEntryPublic)
async def start_reading(
    entry_id: UUID,
    authenticated_user: User = Depends(
        RequirePermission(Permission.EDIT_OWN_READING_ENTRY)
    ),
    service: ReadingEntryService = Depends(get_reading_entry_service),
):
    try:
        entry = await service.start_reading(entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Reading entry not found")
        return ReadingEntryPublic.model_validate(entry)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{entry_id}/progress", response_model=ReadingEntryPublic)
async def update_progress(
    entry_id: UUID,
    request: UpdateProgressRequest,
    authenticated_user: User = Depends(
        RequirePermission(Permission.EDIT_OWN_READING_ENTRY)
    ),
    service: ReadingEntryService = Depends(get_reading_entry_service),
):
    try:
        entry = await service.update_reading_progress(entry_id, request.progress)
        if not entry:
            raise HTTPException(status_code=404, detail="Reading entry not found")
        return ReadingEntryPublic.model_validate(entry)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{entry_id}/review", response_model=ReadingEntryPublic)
async def update_review(
    entry_id: UUID,
    request: UpdateReviewRequest,
    authenticated_user: User = Depends(
        RequirePermission(Permission.EDIT_OWN_READING_ENTRY)
    ),
    service: ReadingEntryService = Depends(get_reading_entry_service),
):
    try:
        entry = await service.update_review(entry_id, request.rating, request.review)
        if not entry:
            raise HTTPException(status_code=404, detail="Reading entry not found")
        return ReadingEntryPublic.model_validate(entry)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{entry_id}/complete", response_model=ReadingEntryPublic)
async def complete_reading(
    entry_id: UUID,
    authenticated_user: User = Depends(
        RequirePermission(Permission.EDIT_OWN_READING_ENTRY)
    ),
    service: ReadingEntryService = Depends(get_reading_entry_service),
):
    entry = await service.complete_reading(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Reading entry not found")
    return ReadingEntryPublic.model_validate(entry)


@router.patch("/{entry_id}/abandon", response_model=ReadingEntryPublic)
async def abandon_reading(
    entry_id: UUID,
    authenticated_user: User = Depends(
        RequirePermission(Permission.EDIT_OWN_READING_ENTRY)
    ),
    service: ReadingEntryService = Depends(get_reading_entry_service),
):
    entry = await service.abandon_reading(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Reading entry not found")
    return ReadingEntryPublic.model_validate(entry)


@router.delete("/{entry_id}", status_code=204)
async def delete_reading_entry(
    entry_id: UUID,
    authenticated_user: User = Depends(
        RequirePermission(Permission.DELETE_OWN_READING_ENTRY)
    ),
    service: ReadingEntryService = Depends(get_reading_entry_service),
):
    success = await service.delete_entry(entry_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reading entry not found")
