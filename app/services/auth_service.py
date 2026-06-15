from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.models import UserModel
from app.schemas.schemas import TokenData, UserCreate

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


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
        logger.debug("User with provided email not found")

    @staticmethod
    def get_password_hash(password: str) -> str:
        pw_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        pw_hashed = bcrypt.hashpw(pw_bytes, salt)
        return pw_hashed.decode("utf-8")

    async def register_user(self, user_data: UserCreate, db: AsyncSession) -> UserModel:
        logger.info("Registering a new user")
        logger.debug("Creating hashed password")
        password_hash = self.get_password_hash(user_data.password)
        new_user = UserModel(email=user_data.email, password=password_hash)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        logger.info(f"Created user with id: {new_user.id}")
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
        logger.info(f"Succesfully authenticated user id: {user.id}")
        return user

    @staticmethod
    def create_access_token(data: dict) -> str:
        logger.debug("Creating user access token")
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.info("Succesfully created user access token")
        return access_token


auth_service = AuthService()


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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
