from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import UserModel


class AssistantBase(ABC):
    @abstractmethod
    async def stream_response(
        self,
        *,
        query_content: str,
        current_user: UserModel,
        db: AsyncSession,
    ) -> AsyncIterator[str]:
        pass
