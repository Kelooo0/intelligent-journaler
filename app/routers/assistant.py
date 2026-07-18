from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_assistant_service, get_current_user, get_db
from app.models.models import UserModel
from app.schemas.schemas import QuerySchema, ResponseSchema
from app.services.ai.assistant.base import AssistantBase

router = APIRouter()


@router.post("")
async def find_matching(
    user_query: QuerySchema,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    assistant_service: AssistantBase = Depends(get_assistant_service),
) -> ResponseSchema:
    return await assistant_service.response(
        query_content=user_query.content, current_user=current_user, db=db
    )
