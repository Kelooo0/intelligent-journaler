from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import UserModel
from app.schemas.schemas import Entry, Tag, VectorResult
from app.services.vector.base import VectorBase


class MockVector(VectorBase):
    async def find_matching(
        self,
        *,
        query_content: str,
        start_date_str: str,
        end_date_str: str,
        current_user: UserModel,
        db: AsyncSession,
    ) -> list[VectorResult]:
        return [
            VectorResult(
                entry=Entry(
                    id=1,
                    content="Example entry content",
                    summary="An example AI generated summary",
                    mood="Neutral",
                    sentiment_score=0.1,
                    tags=[
                        Tag(id=1, name="tag1", user_id=current_user.id),
                        Tag(id=2, name="tag2", user_id=current_user.id),
                        Tag(id=3, name="tag3", user_id=current_user.id),
                    ],
                    created_at=datetime.now(UTC),
                    user_id=current_user.id,
                ),
                relevance_score=0.85,
            ),
            VectorResult(
                entry=Entry(
                    id=2,
                    content="Example entry content",
                    summary="An example AI generated summary",
                    mood="Neutral",
                    sentiment_score=0.1,
                    tags=[
                        Tag(id=1, name="tag1", user_id=current_user.id),
                        Tag(id=2, name="tag2", user_id=current_user.id),
                        Tag(id=3, name="tag3", user_id=current_user.id),
                    ],
                    created_at=datetime.now(UTC),
                    user_id=current_user.id,
                ),
                relevance_score=0.84,
            ),
            VectorResult(
                entry=Entry(
                    id=3,
                    content="Example entry content",
                    summary="An example AI generated summary",
                    mood="Neutral",
                    sentiment_score=0.1,
                    tags=[
                        Tag(id=1, name="tag1", user_id=current_user.id),
                        Tag(id=2, name="tag2", user_id=current_user.id),
                        Tag(id=3, name="tag3", user_id=current_user.id),
                    ],
                    created_at=datetime.now(UTC),
                    user_id=current_user.id,
                ),
                relevance_score=0.83,
            ),
        ]
