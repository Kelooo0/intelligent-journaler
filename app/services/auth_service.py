from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import UserCreate
from passlib.context import CryptContext
from app.config import settings
from app.models import UserModel
from datetime import datetime, timedelta, timezone
import jwt

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')
ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY

class AuthService:
    @staticmethod
    def check_user_exists(email: str, db: Session):
        from app.models import UserModel
        existing_user = db.query(UserModel).filter(UserModel.email == email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')

    @staticmethod
    def get_password_hash(password: str):
        return pwd_context.hash(password)

    def register_user(self, user_data: UserCreate, db: Session):
        password_hash = self.get_password_hash(user_data.password)
        new_user = UserModel(email=user_data.email, password=password_hash)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def verify_password(password: str, password_hash: str):
        return pwd_context.verify(password, password_hash)

    def authenticate_user(self, email: str, password: str, db: Session):
        user = db.query(UserModel).filter(UserModel.email == email).first()
        if not user or not self.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect email or password',
                headers={'WWW-Authentication': 'Bearer'},
                )
        return user

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        to_encode.update({'exp': expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
auth_service=AuthService()
