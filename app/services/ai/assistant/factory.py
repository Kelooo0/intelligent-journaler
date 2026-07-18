from functools import lru_cache

from loguru import logger

from app.core.config import settings
from app.services.ai.assistant.assistant_service import AssistantService
from app.services.ai.assistant.base import AssistantBase
from app.services.ai.assistant.mock_assistant_service import MockAssistantService
from app.services.ai.tools.executor import ToolExecutor


@lru_cache
def assistant_service(executor: ToolExecutor) -> AssistantBase:
    if settings.LLM_PROVIDER == "openai":
        logger.debug("Selected LLM provider for assistant service: OpenAI")
        return AssistantService(executor=executor)
    logger.debug("Selected LLM provider for assistant service: Mock")
    return MockAssistantService()
