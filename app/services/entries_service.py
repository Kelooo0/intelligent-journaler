from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models import UserModel, EntryModel, TagModel
from app.schemas import EntryCreate, EntryUpdate
from typing import Optional
from app.services.ai_service import ai_service
from app.services.tags_service import get_tags_str, process_tags
from datetime import date, timedelta, time, datetime


def get_entries_service(
    db: Session,
    current_user: UserModel,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    tags_list: Optional[list[str]] = None,
) -> list[EntryModel]:
    query = db.query(EntryModel).filter(EntryModel.user_id == current_user.id)
    if start_date:
        start_dt = datetime.combine(start_date, time.min)
        query = query.filter(EntryModel.created_at > start_dt)
    if end_date:
        next_day = end_date + timedelta(days=1)
        end_dt = datetime.combine(next_day, time.min)
        query = query.filter(EntryModel.created_at < end_dt)
    if tags_list:
        cleaned_tags = []
        for t in tags_list:
            t = t.strip().lower()
            if not t:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid tag input, tag can't be empty",
                )
            if len(t) < 3:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid tag input, tag must be at least 3 characters",
                )
            if len(t) > 20:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid tag input, tag must be less than 20 characters",
                )
            cleaned_tags.append(t)
        query = query.filter(EntryModel.tags.any(TagModel.name.in_(cleaned_tags)))
    return query.order_by(EntryModel.created_at.desc()).all()


def create_entry_service(
    entry_data: EntryCreate, db: Session, current_user: UserModel
) -> EntryModel:
    tags = get_tags_str(db, current_user.id)
    analysis = ai_service.analyze_entry(entry_data.content, tags)
    new_entry = EntryModel(
        content=entry_data.content,
        user_id=current_user.id,
        summary=analysis.summary,
        mood=analysis.mood,
        sentiment_score=analysis.sentiment_score,
    )
    db_tags = process_tags(analysis.tags, db, current_user.id)
    new_entry.tags = db_tags
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


def update_entry_service(
    update_data: EntryUpdate, entry: EntryModel, db: Session
) -> EntryModel:
    update_dict = update_data.model_dump(exclude_unset=True)
    new_content = update_dict.get("content")
    content_changed = new_content is not None and new_content != entry.content
    for key, value in update_dict.items():
        setattr(entry, key, value)

    if content_changed:
        tags = get_tags_str(db, entry.user_id)
        analysis = ai_service.analyze_entry(entry.content, tags)
        entry.summary = analysis.summary
        entry.mood = analysis.mood
        entry.sentiment_score = analysis.sentiment_score
        db_tags = process_tags(analysis.tags, db, entry.user_id)
        entry.tags = db_tags
    db.commit()
    return entry


def delete_entry_service(entry: EntryModel, db: Session) -> None:
    db.delete(entry)
    db.commit()
    return None
