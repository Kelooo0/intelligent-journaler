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
from app.services.ai.base import AIService
from app.services.ai.factory import ai_service

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
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> UserModel:
    logger.debug("Fetching current user's database model")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentials error",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        logger.debug("Decoding JWT token")
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            logger.error("No email found in user's payload")
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.PyJWTError:
        logger.error("A PyJWT error occured")
        raise credentials_exception
    user = await db.scalar(select(UserModel).where(UserModel.email == token_data.email))
    if user is None:
        logger.error("User with email fetched from JWT token not found")
        raise credentials_exception
    logger.debug(
        f"Succesfully fetched current user's database model, user id: {user.id}"
    )
    return user


async def validate_entry(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> EntryModel:
    logger.debug("Performing entry validation")
    entry = await db.scalar(select(EntryModel).where(EntryModel.id == id))
    if entry is None:
        logger.debug(f"Entry id: {id} doesn't exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found"
        )
    if entry.user_id != current_user.id:
        logger.debug(
            f"User id: {current_user.id} doesn't have access for entry id: {id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found",
        )
    return entry


def get_ai() -> AIService:
    return ai_service()
