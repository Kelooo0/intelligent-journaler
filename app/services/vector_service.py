from datetime import datetime, time, timedelta

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.models import EntryModel, UserModel
from app.schemas.schemas import DatesSchema, VectorResult
from app.services.ai.base import AIService


async def find_matching_service(
    query_content: str,
    dates: DatesSchema,
    current_user: UserModel,
    db: AsyncSession,
    ai: AIService,
) -> list[VectorResult]:
    logger.debug("Searching for matching entries")
    logger.debug("Generating an embedding for provided query")
    query_embedding = await ai.get_embedding(query_content)
    if query_embedding is None:
        logger.error("An error occured while generating query embedding")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="An error occured while trying to fetch matching entries",
        )
    logger.debug("Building database query")
    database_query = select(
        EntryModel,
        (1 - EntryModel.embedding.cosine_distance(query_embedding)).label("score"),
    ).where(EntryModel.user_id == current_user.id)
    if dates.start_date:
        start_dt = datetime.combine(dates.start_date, time.min)
        database_query = database_query.filter(EntryModel.created_at >= start_dt)
    if dates.end_date:
        next_day = dates.end_date + timedelta(days=1)
        end_dt = datetime.combine(next_day, time.min)
        database_query = database_query.filter(EntryModel.created_at < end_dt)
    database_query = database_query.order_by(
        EntryModel.embedding.cosine_distance(query_embedding)
    ).limit(settings.VECTOR_TOP_K_RETRIEVAL)
    result = await db.execute(database_query)
    results = [
        VectorResult(entry=entry, relevance_score=score)
        for entry, score in result.all()
    ]
    logger.debug(f"Number of rows retrieved: {len(results)}")
    high = [r for r in results if r.relevance_score >= settings.VECTOR_HIGH_TRESHOLD]
    medium = [
        r
        for r in results
        if settings.VECTOR_MEDIUM_TRESHOLD
        <= r.relevance_score
        < settings.VECTOR_HIGH_TRESHOLD
    ]
    if high:
        logger.debug(f"{len(high)} highly matching entries found")
        return high[: settings.VECTOR_TOP_K_FINAL]
    elif medium:
        logger.debug(f"{len(medium)} moderately matching entries found")
        return medium[: settings.VECTOR_TOP_K_FINAL]
    else:
        logger.debug("No enough matching entries found")
        return []
