from functools import lru_cache

from app.core.config import settings
from app.services.vector.base import VectorBase
from app.services.vector.mock_vector_service import MockVector
from app.services.vector.vector_service import VectorService


@lru_cache
def vector_service() -> VectorBase:
    if settings.LLM_PROVIDER == "openai":
        return VectorService()
    return MockVector()
