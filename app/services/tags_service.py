from sqlalchemy.orm import Session
from app.models import TagModel


def get_tags_str(db: Session) -> str:
    existing_tags = db.query(TagModel).all()
    tags_list = [t.name for t in existing_tags]
    return ", ".join(tags_list) if tags_list else "None"


def process_tags(tags: list[str], db: Session) -> list[TagModel]:
    db_tags = []
    for tag in tags:
        clean_tag = tag.lower().strip()
        tag = db.query(TagModel).filter(TagModel.name == clean_tag).first()
        if tag is None:
            tag = TagModel(name=clean_tag)
            db.add(tag)
            db.flush()
        db_tags.append(tag)
    return db_tags
