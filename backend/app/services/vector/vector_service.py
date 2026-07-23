from datetime import datetime, time, timedelta

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.models import EntryModel, UserModel
from app.schemas.schemas import VectorResult
from app.services.ai.base import AIBase
from app.services.vector.base import VectorBase


class VectorService(VectorBase):
    def __init__(self, ai: AIBase) -> None:
        self.ai = ai

    async def find_matching(
        self,
        *,
        query_content: str,
        start_date_str: str,
        end_date_str: str,
        current_user: UserModel,
        db: AsyncSession,
    ) -> list[VectorResult]:
        logger.debug("Searching for matching entries")
        logger.debug("Matching entries start date: {}", start_date_str)
        logger.debug("Matching entries end date: {}", end_date_str)
        query_embedding = await self.ai.get_embedding(query_content)
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
        if start_date_str:
            start_date_dt = datetime.strptime(start_date_str, "%Y-%m-%d")
            start_date = datetime.combine(start_date_dt, time.min)
            database_query = database_query.filter(EntryModel.created_at >= start_date)
            logger.debug("Added start date to database query")
        if end_date_str:
            end_date_dt = datetime.strptime(end_date_str, "%Y-%m-%d")
            next_day = end_date_dt + timedelta(days=1)
            end_date = datetime.combine(next_day, time.min)
            database_query = database_query.filter(EntryModel.created_at < end_date)
            logger.debug("Added end date to database query")
        database_query = database_query.order_by(
            EntryModel.embedding.cosine_distance(query_embedding)
        ).limit(settings.VECTOR_TOP_K_RETRIEVAL)
        result = await db.execute(database_query)
        results = [
            VectorResult(entry=entry, relevance_score=score)
            for entry, score in result.all()
        ]
        logger.debug("Number of rows retrieved: {}", len(results))
        if results:
            high = [
                r for r in results if r.relevance_score >= settings.VECTOR_HIGH_TRESHOLD
            ]
            logger.debug("{} highly matching entries found", len(high))

            medium = [
                r
                for r in results
                if settings.VECTOR_MEDIUM_TRESHOLD
                <= r.relevance_score
                < settings.VECTOR_HIGH_TRESHOLD
            ]
            logger.debug("{} moderately matching entries found", len(medium))

            max_score = results[0].relevance_score
            score_delta = max_score - settings.VECTOR_DELTA

            fallback_matches = [
                r
                for r in results
                if settings.VECTOR_MEDIUM_TRESHOLD
                > r.relevance_score
                >= settings.VECTOR_FALLBACK_TRESHOLD
                and r.relevance_score >= score_delta
            ]
            logger.debug("{} fallback entries found", len(fallback_matches))

            matching_entries = high + medium + fallback_matches

            if matching_entries:
                return matching_entries[: settings.VECTOR_TOP_K_FINAL]

        logger.debug("No enough matching entries found")
        return []
