from app.models.models import EntryModel
from app.schemas.schemas import DatesSchema, EntryAnalysis
from app.services.ai.base import AIService


class AIMockService(AIService):
    async def analyze_entry(self, content: str, tags: str) -> EntryAnalysis:
        return EntryAnalysis(
            summary="Example summary",
            mood="Neutral",
            sentiment_score=0.0,
            tags=["tag1", "tag2", "tag3"],
        )

    async def get_embedding(self, content: str) -> list[float] | None:
        return [0.1] * 768

    async def get_dates(self, query_content: str) -> DatesSchema:
        return DatesSchema(start_date="2026-06-28", end_date="2026-06-28")

    async def transform_query(self, query_content: str) -> str:
        return "Example transformed query"

    async def assistant_response(
        self, query_content: str, matching_entries: list[EntryModel]
    ) -> dict[str, str]:
        return {"answer": "Example assistant answer"}
