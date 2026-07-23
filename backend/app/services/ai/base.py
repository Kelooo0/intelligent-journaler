from abc import ABC, abstractmethod

from app.schemas.schemas import EntryAnalysis


class AIBase(ABC):
    @abstractmethod
    async def analyze_entry(self, content: str, tags: str) -> EntryAnalysis:
        pass

    @abstractmethod
    async def get_embedding(self, content: str) -> list[float] | None:
        pass
