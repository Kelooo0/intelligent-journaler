from app.schemas.schemas import (
    DatesSchema,
    EntryAnalysis,
    ResponseSchema,
    UsedEntry,
    VectorResult,
)
from app.services.ai.base import AIService


class AIMockService(AIService):
    async def analyze_entry(self, content: str, tags: str) -> EntryAnalysis:
        return EntryAnalysis(
            summary="An example AI generated summary",
            mood="Neutral",
            sentiment_score=0.1,
            tags=["tag1", "tag2", "tag3"],
        )

    async def get_embedding(self, content: str) -> list[float] | None:
        return [0.1] * 1536

    async def get_dates(self, query_content: str) -> DatesSchema:
        return DatesSchema(start_date="2026-06-28", end_date="2026-06-28")

    async def transform_query(self, query_content: str) -> str:
        return "Example transformed user query"

    async def assistant_response(
        self, query_content: str, vector_result: list[VectorResult]
    ) -> ResponseSchema:
        return ResponseSchema(
            answer="Example AI assistent response",
            used_entries=[
                UsedEntry(
                    id=vector_result[0].entry.id,
                    relevance_score=vector_result[0].relevance_score,
                ),
                UsedEntry(
                    id=vector_result[1].entry.id,
                    relevance_score=vector_result[1].relevance_score,
                ),
                UsedEntry(
                    id=vector_result[2].entry.id,
                    relevance_score=vector_result[2].relevance_score,
                ),
            ],
            intent="emotional_reflection",
        )
