from app.schemas.schemas import (
    EntryAnalysis,
)
from app.services.ai.base import AIBase


class AIMockService(AIBase):
    async def analyze_entry(self, content: str, tags: str) -> EntryAnalysis:
        return EntryAnalysis(
            summary="An example AI generated summary",
            mood="Neutral",
            sentiment_score=0.1,
            tags=["tag1", "tag2", "tag3"],
        )

    async def get_embedding(self, content: str) -> list[float] | None:
        return [0.1] * 1536
