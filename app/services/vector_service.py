from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import EntryModel, UserModel
from app.services.ai_service import ai_service


async def find_similar_service(
    query: str, current_user: UserModel, db: AsyncSession
) -> list[EntryModel]:
    logger.info("Searching for matching entries")
    clean_query = query.strip()
    if not clean_query:
        logger.error("User provided query with only empty spaces")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content can't be an empty spaces",
        )
    logger.debug("Generating an embedding for provided query")
    query_embedding = await ai_service.get_embedding(clean_query)
    if query_embedding is None:
        logger.error("An error occured while generating query embedding")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="An error occured while trying to fetch similar entries",
        )
    database_query = (
        select(EntryModel)
        .where(EntryModel.user_id == current_user.id)
        .order_by(EntryModel.embedding.cosine_distance(query_embedding))
        .limit(5)
    )
    result = await db.execute(database_query)
    logger.info("Returning matching entries")
    return result.scalars().all()
