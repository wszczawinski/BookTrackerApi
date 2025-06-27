from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.reading_entry import (
    ReadingEntry,
    ReadingEntryCreate,
    ReadingEntryUpdate,
    ReadingStatus,
)

router = APIRouter()


@router.post("/", response_model=ReadingEntry)
def create_reading_entry(
    entry: ReadingEntryCreate, session: Session = Depends(get_session)
):
    db_entry = ReadingEntry.model_validate(entry)
    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)
    return db_entry


@router.get("/", response_model=List[ReadingEntry])
def get_reading_entries(
    status: Optional[ReadingStatus] = Query(None),
    session: Session = Depends(get_session),
):
    query = select(ReadingEntry)
    if status:
        query = query.where(ReadingEntry.status == status)
    return session.exec(query).all()


@router.patch("/{entry_id}", response_model=ReadingEntry)
def update_reading_entry(
    entry_id: UUID,
    entry_update: ReadingEntryUpdate,
    session: Session = Depends(get_session),
):
    db_entry = session.get(ReadingEntry, entry_id)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Reading entry not found")

    update_data = entry_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_entry, key, value)

    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)
    return db_entry
