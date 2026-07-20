from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import UserModel
from app.services.ai.assistant.base import AssistantBase


class MockAssistantService(AssistantBase):
    async def stream_response(
        self,
        *,
        query_content: str,
        current_user: UserModel,
        db: AsyncSession,
    ) -> AsyncIterator[str]:
        yield "This is a mock assistant response"
