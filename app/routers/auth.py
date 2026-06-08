from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import Token, User, UserCreate
from app.services.auth_service import auth_service

router = APIRouter()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    await auth_service.check_user_exists(user_data.email, db)
    return await auth_service.register_user(user_data, db)


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> Token:
    user = await auth_service.authenticate_user(
        form_data.username, form_data.password, db
    )

    access_token = auth_service.create_access_token(data={"sub": user.email})
    token = Token(access_token=access_token, token_type="bearer")
    return token
