from sqlalchemy.orm import Session
from app.models import UserModel, EntryModel
from app.schemas import EntryCreate, EntryUpdate
from typing import List
from app.services.ai_service import ai_service
from app.services.tags_service import get_tags_str, process_tags


def get_entries_service(db: Session, current_user: UserModel) -> List[EntryModel]:
    entries = db.query(EntryModel).filter(EntryModel.user_id == current_user.id).all()
    return entries


def create_entry_service(
    entry_data: EntryCreate, db: Session, current_user: UserModel
) -> EntryModel:
    tags = get_tags_str(db)
    analysis = ai_service.analyze_entry(entry_data.content, tags)
    new_entry = EntryModel(
        content=entry_data.content,
        user_id=current_user.id,
        summary=analysis.summary,
        mood=analysis.mood,
        sentiment_score=analysis.sentiment_score,
    )
    db_tags = process_tags(analysis.tags, db)
    new_entry.tags = db_tags
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


def update_entry_service(
    update_data: EntryUpdate, entry: EntryModel, db: Session
) -> EntryModel:
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(entry, key, value)
    new_content = update_dict.get("content")
    if new_content is not None and new_content != entry.content:
        tags = get_tags_str(db)
        analysis = ai_service.analyze_entry(entry.content, tags)
        entry.summary = analysis.summary
        entry.mood = analysis.mood
        entry.sentiment_score = analysis.sentiment_score
        db_tags = process_tags(analysis.tags, db)
        entry.tags = db_tags
    db.commit()
    return entry


def delete_entry_service(entry: EntryModel, db: Session) -> None:
    db.delete(entry)
    db.commit()
    return None
