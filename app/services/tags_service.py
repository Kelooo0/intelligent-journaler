from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TagModel


async def get_tags_str(db: AsyncSession, user_id: int) -> str:
    existing_tags = (await db.scalars(select(TagModel))).all()
    tags_list = [t.name for t in existing_tags]
    return ", ".join(tags_list) if tags_list else "None"


async def process_tags(
    tags: list[str], db: AsyncSession, user_id: int
) -> list[TagModel]:
    db_tags = []
    for tag in tags:
        clean_tag = tag.lower().strip()
        tag = await db.scalar(
            select(TagModel).filter(
                TagModel.user_id == user_id, TagModel.name == clean_tag
            )
        )
        if tag is None:
            tag = TagModel(user_id=user_id, name=clean_tag)
            db.add(tag)
            await db.flush()
        db_tags.append(tag)
    return db_tags
