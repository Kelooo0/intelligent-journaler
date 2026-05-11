from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str

class EntryBase(BaseModel):
    content: str


class EntryCreate(EntryBase):
    pass

class EntryUpdate(EntryBase):
    content: Optional[str] = None

class Entry(EntryBase):
    id: int
    user_id: int
    content: str
    summary: Optional[str] = None
    mood: Optional[str] = None
    sentiment_score: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True
