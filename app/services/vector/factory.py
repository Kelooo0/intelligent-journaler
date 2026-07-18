from functools import lru_cache

from loguru import logger

from app.core.config import settings
from app.services.ai.base import AIBase
from app.services.vector.base import VectorBase
from app.services.vector.mock_vector_service import MockVector
from app.services.vector.vector_service import VectorService


@lru_cache
def vector_service(ai: AIBase) -> VectorBase:
    if settings.LLM_PROVIDER == "openai":
        logger.debug("Selected LLM provider: OpenAI")
        return VectorService(ai=ai)
    logger.debug("Selected LLM provider: Mock")
    return MockVector()
