from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import TagModel


class TagService:
    @staticmethod
    async def get_tags_str(db: AsyncSession, user_id: int) -> str:
        logger.debug("Fetching existing tags for user_id: {}", user_id)
        existing_tags = (
            await db.scalars(select(TagModel).where(TagModel.user_id == user_id))
        ).all()
        tags_list = [t.name for t in existing_tags]
        logger.debug(f"{len(tags_list)} tags have been found")
        return ", ".join(tags_list) if tags_list else "None"

    @staticmethod
    async def process_tags(
        tags: list[str], db: AsyncSession, user_id: int
    ) -> list[TagModel]:
        logger.debug("Processing tags returned from the AI analysis")
        db_tags = []
        for tag in tags:
            clean_tag = tag.lower().strip()
            tag = await db.scalar(
                select(TagModel).filter(
                    TagModel.user_id == user_id, TagModel.name == clean_tag
                )
            )
            if tag is None:
                logger.debug("Adding a new tag to database: {}", clean_tag)
                tag = TagModel(user_id=user_id, name=clean_tag)
                db.add(tag)
                await db.flush()
            db_tags.append(tag)
        logger.debug(
            "Returning a list of processed tag objects with {} elements", len(db_tags)
        )
        return db_tags
