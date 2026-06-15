from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import EntryModel, UserModel
from app.schemas import Entry, EntryCreate, EntryUpdate
from app.services.auth_service import get_current_user
from app.services.entries_service import (
    create_entry_service,
    delete_entry_service,
    get_entries_service,
    update_entry_service,
)

router = APIRouter()


async def validate_entry(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> EntryModel:
    logger.debug("Performing entry validation")
    entry = await db.scalar(select(EntryModel).where(EntryModel.id == id))
    if entry is None:
        logger.debug(f"Entry id: {id} doesn't exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found"
        )
    if entry.user_id != current_user.id:
        logger.debug(
            f"User id: {current_user.id} doesn't have access for entry id: {id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found",
        )
    return entry


@router.get("", response_model=list[Entry])
async def get_entries(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
    start_date: date | None = None,
    end_date: date | None = None,
    tags: list[str] | None = Query(
        None,
        min_length=1,
        max_length=5,
        description="Add up to 5 tags (optional). Each tag between 3 and 20 characters.",
    ),
) -> list[Entry]:
    return await get_entries_service(db, current_user, start_date, end_date, tags)


@router.get("/{id}", response_model=Entry)
async def get_entry(entry: EntryModel = Depends(validate_entry)) -> Entry:
    logger.info(f"Returning entry data for entry id: {entry.id}")
    return entry


@router.post("", response_model=Entry, status_code=status.HTTP_201_CREATED)
async def create_entry(
    entry_data: EntryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> Entry:
    return await create_entry_service(entry_data, db, current_user)


@router.patch("/{id}", response_model=Entry)
async def update_entry(
    update_data: EntryUpdate,
    entry: EntryModel = Depends(validate_entry),
    db: AsyncSession = Depends(get_db),
) -> Entry:
    return await update_entry_service(update_data, entry, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entry(
    entry: EntryModel = Depends(validate_entry), db: AsyncSession = Depends(get_db)
) -> None:
    return await delete_entry_service(entry, db)
