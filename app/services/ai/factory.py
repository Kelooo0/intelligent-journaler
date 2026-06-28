from functools import lru_cache

from loguru import logger

from app.core.config import settings
from app.services.ai.base import AIService
from app.services.ai.gemini_service import GeminiService
from app.services.ai.mock_service import AIMockService
from app.services.ai.openai_service import OpenAIService


@lru_cache
def ai_service() -> AIService:
    if settings.LLM_PROVIDER == "openai":
        logger.debug("Selected LLM provider: OpenAI")
        return OpenAIService()
    elif settings.LLM_PROVIDER == "mock":
        logger.debug("Selected LLM provider: Mock")
        return AIMockService()
    logger.debug("Selected LLM provider: Gemini")
    return GeminiService()
