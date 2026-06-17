from datetime import date, datetime, time, timedelta

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import EntryModel, TagModel, UserModel
from app.schemas.schemas import EntryCreate, EntryUpdate
from app.services.ai_service import ai_service
from app.services.tags_service import get_tags_str, process_tags


async def get_entries_service(
    db: AsyncSession,
    current_user: UserModel,
    start_date: date | None = None,
    end_date: date | None = None,
    tags_list: list[str] | None = None,
) -> list[EntryModel]:
    logger.debug(f"Fetching all entries for user id: {current_user.id}")
    logger.debug("Building a database query")
    query = select(EntryModel).where(EntryModel.user_id == current_user.id)
    if start_date:
        start_dt = datetime.combine(start_date, time.min)
        query = query.filter(EntryModel.created_at >= start_dt)
        logger.debug("Added start date to database query")
    if end_date:
        next_day = end_date + timedelta(days=1)
        end_dt = datetime.combine(next_day, time.min)
        query = query.filter(EntryModel.created_at < end_dt)
        logger.debug("Added end date to database query")
    if tags_list:
        logger.debug("Validating provided tags")
        cleaned_tags = []
        for t in tags_list:
            t = t.strip().lower()
            if not t:
                logger.error("User provided an empty tag")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid tag input, tag can't be empty",
                )
            if len(t) < 3:
                logger.error(f"User provided a too short tag name: {t}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{t} is invalid, tag must be at least 3 characters",
                )
            if len(t) > 20:
                logger.error(f"User provided a too long tag name: {t}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{t} is invalid, tag must be less than 20 characters",
                )
            cleaned_tags.append(t)
        query = query.filter(EntryModel.tags.any(TagModel.name.in_(cleaned_tags)))
    query = query.order_by(EntryModel.created_at.desc())
    logger.debug("Executing the database query")
    result = await db.execute(query)
    logger.info("Returning a list of fetched entries")
    return result.scalars().all()


async def create_entry_service(
    entry_data: EntryCreate, db: AsyncSession, current_user: UserModel
) -> EntryModel:
    logger.info(f"Creating a new entry for user id: {current_user.id}")
    tags = await get_tags_str(db, current_user.id)
    analysis = await ai_service.analyze_entry(entry_data.content, tags)
    embedding = await ai_service.get_embedding(entry_data.content)
    new_entry = EntryModel(
        content=entry_data.content,
        user_id=current_user.id,
        summary=analysis.summary,
        mood=analysis.mood,
        sentiment_score=analysis.sentiment_score,
        embedding=embedding,
    )
    logger.debug("Created a new entry object")
    db_tags = await process_tags(analysis.tags, db, current_user.id)
    new_entry.tags = db_tags
    logger.debug("Assigned tags to a new entry object")
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)
    logger.info(f"Succesfully added a new entry to database, entry id: {new_entry.id}")
    return new_entry


async def update_entry_service(
    update_data: EntryUpdate, entry: EntryModel, db: AsyncSession
) -> EntryModel:
    logger.debug(f"Updating entry id: {entry.id}")
    update_dict = update_data.model_dump(exclude_unset=True)
    new_content = update_dict.get("content")
    content_changed = new_content is not None and new_content != entry.content
    logger.debug("Assigning new values")
    for key, value in update_dict.items():
        setattr(entry, key, value)
    logger.debug("Checking for changed entry content")
    if content_changed:
        logger.debug(f"Generating a new analysis for entry id: {entry.id} ")
        tags = await get_tags_str(db, entry.user_id)
        analysis = await ai_service.analyze_entry(entry.content, tags)
        embedding = await ai_service.get_embedding(entry.content)
        logger.debug("Updating ai analysis data")
        entry.summary = analysis.summary
        entry.mood = analysis.mood
        entry.sentiment_score = analysis.sentiment_score
        entry.embedding = embedding
        db_tags = await process_tags(analysis.tags, db, entry.user_id)
        entry.tags = db_tags
        logger.debug("Assigned updated tags")
    await db.commit()
    logger.info(f"Entry updated succesfully, entry id: {entry.id}")
    return entry


async def delete_entry_service(entry: EntryModel, db: AsyncSession) -> None:
    logger.debug(f"Deleting entry id: {entry.id}")
    await db.delete(entry)
    await db.commit()
    logger.info("Entry deleted succesfully")
    return None
