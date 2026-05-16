from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class EntryBase(BaseModel):
    content: str = Field(..., min_length=30)

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Invalid content")
        return v


class EntryCreate(EntryBase):
    pass


class EntryUpdate(EntryBase):
    content: Optional[str] = Field(None, min_length=30)


class Tag(BaseModel):
    id: int
    user_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class Entry(EntryBase):
    id: int
    user_id: int
    content: str
    summary: Optional[str] = None
    mood: Optional[str] = None
    sentiment_score: Optional[float] = None
    created_at: datetime
    tags: list[Tag] = []

    model_config = ConfigDict(from_attributes=True)


class EntryAnalysis(BaseModel):
    summary: str = "Analysis unavailable"
    mood: str = "Unknown"
    sentiment_score: float = 0.0
    tags: list[str] = Field(default_factory=list)
