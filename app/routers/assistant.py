from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.models import UserModel
from app.services.ai_service import ai_service
from app.services.vector_service import find_matching_service

router = APIRouter()


@router.post("")
async def find_matching(
    query: str = Body(..., min_length=3, max_length=500),
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    matching_entries = await find_matching_service(query, current_user, db)
    if not matching_entries:
        return {"answer": "I haven't found matching entries for provided query"}
    return await ai_service.assistant_response(query, matching_entries)
