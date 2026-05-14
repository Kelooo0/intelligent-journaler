from sqlalchemy.orm import Session
from app.models import TagModel


def get_tags_str(db: Session, user_id: int) -> str:
    existing_tags = db.query(TagModel).filter(TagModel.user_id == user_id).all()
    tags_list = [t.name for t in existing_tags]
    return ", ".join(tags_list) if tags_list else "None"


def process_tags(tags: list[str], db: Session, user_id: int) -> list[TagModel]:
    db_tags = []
    for tag in tags:
        clean_tag = tag.lower().strip()
        tag = (
            db.query(TagModel)
            .filter(TagModel.user_id == user_id, TagModel.name == clean_tag)
            .first()
        )
        if tag is None:
            tag = TagModel(user_id=user_id, name=clean_tag)
            db.add(tag)
            db.flush()
        db_tags.append(tag)
    return db_tags
