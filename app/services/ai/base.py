from abc import ABC, abstractmethod

from app.schemas.schemas import DatesSchema, EntryAnalysis, ResponseSchema, VectorResult


class AIService(ABC):
    @abstractmethod
    async def analyze_entry(self, content: str, tags: str) -> EntryAnalysis:
        pass

    @abstractmethod
    async def get_embedding(self, content: str) -> list[float] | None:
        pass

    @abstractmethod
    async def get_dates(self, query_content: str) -> DatesSchema:
        pass

    @abstractmethod
    async def transform_query(self, query_content: str) -> str:
        pass

    @abstractmethod
    async def assistant_response(
        self, query_content: str, vector_result: list[VectorResult]
    ) -> ResponseSchema:
        pass
