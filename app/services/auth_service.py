from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.models import UserModel
from app.schemas.schemas import UserCreate


class AuthService:
    @staticmethod
    async def check_user_exists(email: str, db: AsyncSession) -> None:
        logger.debug("Checking if user already exists")
        from app.models.models import UserModel

        existing_user = await db.scalar(
            select(UserModel).where(UserModel.email == email)
        )
        if existing_user:
            logger.error("User already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )
        logger.info("User with provided email not found")

    @staticmethod
    def get_password_hash(password: str) -> str:
        logger.debug("Creating hashed password")
        pw_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        pw_hashed = bcrypt.hashpw(pw_bytes, salt)
        return pw_hashed.decode("utf-8")

    async def register_user(self, user_data: UserCreate, db: AsyncSession) -> UserModel:
        logger.info("Registering a new user")
        password_hash = self.get_password_hash(user_data.password)
        new_user = UserModel(email=user_data.email, password=password_hash)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        logger.info("Created user with id: {}", new_user.id)
        return new_user

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

    async def authenticate_user(
        self, email: str, password: str, db: AsyncSession
    ) -> UserModel:
        logger.debug("Authenticating user logging data")
        user = await db.scalar(select(UserModel).where(UserModel.email == email))
        if not user or not self.verify_password(password, user.password):
            logger.error("User authentication error, incorrect email or password")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authentication": "Bearer"},
            )
        logger.info("Succesfully authenticated user_id: {}", user.id)
        return user

    @staticmethod
    def create_access_token(data: dict) -> str:
        logger.debug("Creating user access token")
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        access_token = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        logger.info("Succesfully created user access token")
        return access_token


auth_service = AuthService()
