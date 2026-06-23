from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.models import UserModel
from app.schemas.schemas import QuerySchema
from app.services.ai_service import ai_service
from app.services.vector_service import find_matching_service

router = APIRouter()


@router.post("")
async def find_matching(
    user_query: QuerySchema,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    dates = await ai_service.get_dates(user_query.content)
    matching_entries = await find_matching_service(
        user_query.content, dates, current_user, db
    )
    if not matching_entries:
        return {"answer": "I haven't found matching entries for provided query"}
    return await ai_service.assistant_response(user_query.content, matching_entries)
