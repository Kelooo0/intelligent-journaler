from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.models import UserModel
from app.schemas.schemas import AssistentSearch, Entry
from app.services.vector_service import find_similar_service

router = APIRouter()


@router.post("", response_model=list[Entry])
async def find_similar(
    search: AssistentSearch,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await find_similar_service(search.query, current_user, db)
