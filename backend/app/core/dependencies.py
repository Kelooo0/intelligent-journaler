from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.models import EntryModel, UserModel
from app.schemas.schemas import TokenData
from app.services.ai.assistant.base import AssistantBase
from app.services.ai.assistant.factory import assistant_service
from app.services.ai.base import AIBase
from app.services.ai.factory import ai_service
from app.services.ai.tools.executor import ToolExecutor
from app.services.entries_service import EntryService
from app.services.tags_service import TagService
from app.services.vector.base import VectorBase
from app.services.vector.factory import vector_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


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


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]
) -> UserModel:
    logger.debug("Fetching current user's database model")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentials error",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        logger.debug("Decoding JWT token")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            logger.error("No email found in user's payload")
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.PyJWTError:
        logger.error("A PyJWT error occured")
        raise credentials_exception from None
    user = await db.scalar(select(UserModel).where(UserModel.email == token_data.email))
    if user is None:
        logger.error("User not found")
        raise credentials_exception
    logger.debug("Succesfully fetched current user's database model for user_id: {}", user.id)
    return user


async def validate_entry(
    id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[UserModel, Depends(get_current_user)],
) -> EntryModel:
    logger.debug("Performing entry validation")
    entry = await db.scalar(select(EntryModel).where(EntryModel.id == id))
    if entry is None:
        logger.debug("Entry with id: {} doesn't exist", id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    if entry.user_id != current_user.id:
        logger.debug("User with id: {} doesn't have access for entry id: {}", current_user.id, id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found",
        )
    return entry


def get_ai_service() -> AIBase:
    return ai_service()


def get_vector_service(ai: Annotated[AIBase, Depends(get_ai_service)]) -> VectorBase:
    return vector_service(ai=ai)


def get_tag_service() -> TagService:
    return TagService()


def get_entry_service(
    ai: Annotated[AIBase, Depends(get_ai_service)],
    tag: Annotated[TagService, Depends(get_tag_service)],
) -> EntryService:
    return EntryService(ai=ai, tag=tag)


def get_tool_executor(
    vector: Annotated[VectorBase, Depends(get_vector_service)],
    entry: Annotated[EntryService, Depends(get_entry_service)],
) -> ToolExecutor:
    return ToolExecutor(vector=vector, entry=entry)


def get_assistant_service(
    executor: Annotated[ToolExecutor, Depends(get_tool_executor)],
) -> AssistantBase:
    return assistant_service(executor=executor)
