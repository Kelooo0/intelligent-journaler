from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import UserModel
from app.schemas.schemas import (
    ResponseSchema,
)
from app.services.ai.assistant.base import AssistantBase


class MockAssistantService(AssistantBase):
    async def response(
        self,
        *,
        query_content: str,
        current_user: UserModel,
        db: AsyncSession,
    ) -> ResponseSchema:
        return ResponseSchema(answer="Example AI assistent response")
