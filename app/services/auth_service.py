from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models import UserModel
from app.schemas import TokenData, UserCreate

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class AuthService:
    @staticmethod
    async def check_user_exists(email: str, db: AsyncSession) -> None:
        from app.models import UserModel

        existing_user = await db.scalar(
            select(UserModel).where(UserModel.email == email)
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    async def register_user(self, user_data: UserCreate, db: AsyncSession) -> UserModel:
        password_hash = self.get_password_hash(user_data.password)
        new_user = UserModel(email=user_data.email, password=password_hash)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return pwd_context.verify(password, password_hash)

    async def authenticate_user(
        self, email: str, password: str, db: AsyncSession
    ) -> UserModel:

        user = await db.scalar(select(UserModel).where(UserModel.email == email))
        if not user or not self.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authentication": "Bearer"},
            )
        return user

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


auth_service = AuthService()


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentials error",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.PyJWTError:
        raise credentials_exception
    user = await db.scalar(select(UserModel).where(UserModel.email == token_data.email))
    if user is None:
        raise credentials_exception
    return user
