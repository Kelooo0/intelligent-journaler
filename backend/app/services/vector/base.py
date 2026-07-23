from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import UserModel
from app.schemas.schemas import VectorResult


class VectorBase(ABC):
    @abstractmethod
    async def find_matching(
        self,
        query_content: str,
        start_date_str: str,
        end_date_str: str,
        current_user: UserModel,
        db: AsyncSession,
    ) -> list[VectorResult]:
        pass
