from functools import lru_cache

from loguru import logger

from app.core.config import settings
from app.services.ai.base import AIService
from app.services.ai.mock_ai_service import AIMockService
from app.services.ai.openai_service import OpenAIService


@lru_cache
def ai_service() -> AIService:
    if settings.LLM_PROVIDER == "openai":
        logger.debug("Selected LLM provider: OpenAI")
        return OpenAIService()
    logger.debug("Selected LLM provider: Mock")
    return AIMockService()
