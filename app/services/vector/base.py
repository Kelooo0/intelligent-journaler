from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import UserModel
from app.schemas.schemas import DatesSchema, VectorResult
from app.services.ai.base import AIService


class VectorBase(ABC):
    @abstractmethod
    async def find_matching_service(
        self,
        query_content: str,
        dates: DatesSchema,
        current_user: UserModel,
        db: AsyncSession,
        ai: AIService,
    ) -> list[VectorResult]:
        pass
