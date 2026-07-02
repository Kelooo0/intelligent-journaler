from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class EntryBase(BaseModel):
    content: str = Field(min_length=30, max_length=10000)

    @field_validator("content", mode="before")
    @classmethod
    def validate_content(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Content can not be empty or just whitespaces")
        return v


class EntryCreate(EntryBase):
    pass


class EntryUpdate(EntryBase):
    content: str | None = Field(default=None, min_length=30, max_length=10000)


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


class QuerySchema(BaseModel):
    content: str = Field(min_length=3, max_length=500)

    @field_validator("content", mode="before")
    @classmethod
    def validate_query(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("User query can not be empty or just whitespaces")
        return v


class DatesSchema(BaseModel):
    start_date: datetime | None = Field(
        default=None,
        description="ISO date YYYY-MM-DD if user specified a time start range",
    )
    end_date: datetime | None = Field(
        default=None,
        description="ISO date YYYY-MM-DD if user specified a time end range",
    )


class UsedEntry(BaseModel):
    id: int = Field(
        description="Unique identifier of the journal entry from the database."
    )
    relevance_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Vector similarity score indicating how relevant this entry is"
        " to the user query. Higher means more relevant.",
    )


class ResponseSchema(BaseModel):
    answer: str = Field(
        default="I couldn't find any relevant journal entries that would fit your query.",
        description="Final response to the user query. Must be a natural language"
        " answer based only on provided journal entries.",
    )
    used_entries: list[UsedEntry] = Field(
        default_factory=list,
        description="List of journal entries used to generate the answer, ranked"
        " by relevance. Each entry includes its ID and similarity score from vector search.",
    )
    intent: str = Field(
        default="memory_recall",
        description="Detected user intent. Examples: memory_recall,"
        " emotional_reflection, advice, general_chat.",
    )


class VectorResult(BaseModel):
    entry: Entry
    relevance_score: float
