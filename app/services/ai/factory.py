from functools import lru_cache

from loguru import logger

from app.core.config import settings
from app.services.ai.ai_service import AIService
from app.services.ai.base import AIBase
from app.services.ai.mock_ai_service import AIMockService


@lru_cache
def ai_service() -> AIBase:
    if settings.LLM_PROVIDER == "openai":
        logger.debug("Selected LLM provider for AI service: OpenAI")
        return AIService()
    logger.debug("Selected LLM provider for AI service: Mock")
    return AIMockService()
