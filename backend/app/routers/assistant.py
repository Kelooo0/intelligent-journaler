from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_assistant_service, get_current_user, get_db
from app.models.models import UserModel
from app.schemas.schemas import QuerySchema
from app.services.ai.assistant.base import AssistantBase

router = APIRouter()


@router.post("")
async def assistant_response(
    user_query: QuerySchema,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    assistant_service: AssistantBase = Depends(get_assistant_service),
) -> StreamingResponse:
    return StreamingResponse(
        assistant_service.stream_response(
            query_content=user_query.content, current_user=current_user, db=db
        ),
        media_type="text/plain; charset=utf-8",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
