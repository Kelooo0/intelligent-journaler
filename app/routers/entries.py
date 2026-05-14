from fastapi import APIRouter, Depends, status, HTTPException, Query
from app.schemas import Entry, EntryCreate, EntryUpdate
from app.database import get_db
from app.models import UserModel
from app.services.auth_service import get_current_user
from sqlalchemy.orm import Session
from app.services.entries_service import (
    get_entries_service,
    create_entry_service,
    update_entry_service,
    delete_entry_service,
)
from app.models import EntryModel
from datetime import date
from typing import Optional

router = APIRouter()


def validate_entry(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> EntryModel:
    entry = db.query(EntryModel).filter(EntryModel.id == id).first()
    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found"
        )
    if entry.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this resource",
        )
    return entry


@router.get("/", response_model=list[Entry])
def get_entries(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    tags: Optional[list[str]] = Query(
        None, min_length=1, max_length=5, description="Add up to 5 tags (optional)"
    ),
) -> list[EntryModel]:
    return get_entries_service(db, current_user, start_date, end_date, tags)


@router.get("/{id}", response_model=Entry)
def get_entry(
    entry: EntryModel = Depends(validate_entry), db: Session = Depends(get_db)
) -> EntryModel:
    return entry


@router.post("/", response_model=Entry, status_code=status.HTTP_201_CREATED)
def create_entry(
    entry_data: EntryCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> EntryModel:
    return create_entry_service(entry_data, db, current_user)


@router.patch("/{id}", response_model=Entry)
def update_entry(
    update_data: EntryUpdate,
    entry: EntryModel = Depends(validate_entry),
    db: Session = Depends(get_db),
) -> EntryModel:
    return update_entry_service(update_data, entry, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(
    entry: EntryModel = Depends(validate_entry), db: Session = Depends(get_db)
) -> None:
    return delete_entry_service(entry, db)
