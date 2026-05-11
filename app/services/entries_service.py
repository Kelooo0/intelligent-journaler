from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import UserModel, EntryModel
from app.schemas import EntryCreate, EntryUpdate
from typing import List

def get_entries_service(db: Session, current_user: UserModel) -> List[EntryModel]:
    entries = db.query(EntryModel).filter(EntryModel.user_id == current_user.id).all()
    return entries

def create_entry_service(entry_data: EntryCreate, db: Session, current_user: UserModel) -> EntryModel:
    #Here will be a function that will generate a summary, mood and sentiment score
    new_entry = EntryModel(
        content=entry_data.content,
        user_id=current_user.id
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

def update_entry_service(update_data: EntryUpdate, entry: EntryModel, db: Session) -> EntryModel:
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(entry, key, value)
    #Here will be a function that will generate new summary, mood, sentiment score based on updated content
    return entry

def delete_entry_service(entry: EntryModel, db: Session) -> None:
    db.delete(entry)
    db.commit()
    return None
