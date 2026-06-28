from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_ai, get_current_user, get_db
from app.models.models import UserModel
from app.schemas.schemas import QuerySchema
from app.services.ai.base import AIService
from app.services.vector_service import find_matching_service

router = APIRouter()


@router.post("")
async def find_matching(
    user_query: QuerySchema,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    ai: AIService = Depends(get_ai),
) -> dict[str, str]:
    dates = await ai.get_dates(user_query.content)
    matching_entries = await find_matching_service(
        user_query.content, dates, current_user, db, ai
    )
    if not matching_entries:
        return {"answer": "I haven't found matching entries for provided query"}
    return await ai.assistant_response(user_query.content, matching_entries)
