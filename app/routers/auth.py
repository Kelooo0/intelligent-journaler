from fastapi import APIRouter, Depends
from app.schemas import UserCreate, User, Token
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import auth_service
from fastapi.security import OAuth2PasswordRequestForm
from app.models import UserModel
from typing import Any

router = APIRouter()


@router.post("/register", response_model=User, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)) -> UserModel:
    auth_service.check_user_exists(user_data.email, db)
    return auth_service.register_user(user_data, db)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Any:
    user = auth_service.authenticate_user(form_data.username, form_data.password, db)

    access_token = auth_service.create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
