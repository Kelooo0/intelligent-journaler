from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import UserModel
from app.schemas.schemas import ResponseSchema


class AssistantBase(ABC):
    @abstractmethod
    async def response(
        self,
        query_content: str,
        current_user: UserModel,
        db: AsyncSession,
    ) -> ResponseSchema:
        pass
