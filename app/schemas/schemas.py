from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


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
    content: str | None = Field(None, min_length=30)


class Tag(BaseModel):
    id: int
    user_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class Entry(EntryBase):
    id: int
    user_id: int
    content: str
    summary: str | None = None
    mood: str | None = None
    sentiment_score: float | None = None
    created_at: datetime
    tags: list[Tag] = []

    model_config = ConfigDict(from_attributes=True)


class EntryAnalysis(BaseModel):
    summary: str = Field(
        default="Analysis unavailable",
        description="Create a very short summary (max 30 chars)",
    )
    mood: str = Field(
        default="Unknown", description="Identify the predominant emotion in one word"
    )
    sentiment_score: float = Field(
        default=0.0, description="Score it from -1.0 (negative) to 1.0 (positive)"
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Generate up to 5 relevant tags."
        " Use matching tags from 'Available existing tags' if they fit;"
        " otherwise, create new ones in the same language "
        "as the content (nominative case)",
    )


class AssistentSearch(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)
