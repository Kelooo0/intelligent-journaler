from fastapi import HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

logger.info("Initializing database engine")

engine = create_async_engine(settings.DATABASE_URL)

SessionLocal = async_sessionmaker(
    autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_db():
    logger.debug("Opening a new database session")
    try:
        async with SessionLocal() as db:
            yield db
    except HTTPException:
        raise
    except Exception:
        logger.exception("Database session error occured")
        raise
    finally:
        logger.debug("Database session closed")
