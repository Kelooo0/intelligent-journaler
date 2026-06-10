import sys

from loguru import logger

from app.config import settings


def setup_logging():
    logger.remove()

    logger.add(
        sys.stdout,
        format=
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level>"
        " | <cyan>ReqID: {extra[request_id]}</cyan> |"
        " <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.LOG_LEVEL,
        filter=lambda record: record["extra"].setdefault("request_id", "GLOBAL"),
    )
    return logger
