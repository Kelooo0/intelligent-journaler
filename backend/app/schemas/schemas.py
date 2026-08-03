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


class Tag(BaseModel):
    id: int
    user_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


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
        description=(
            "A concise factual summary of the journal entry, written in the same "
            "language as the content. Maximum 30 characters. Do not add information "
            "that is not present in the entry."
        ),
    )

    mood: str = Field(
        default="Unknown",
        description=(
            "The predominant emotion or mood expressed in the journal entry, "
            "returned as one concise word in the same language as the content. "
            "Do not infer a specific emotion when the text does not support it."
        ),
    )

    sentiment_score: float = Field(
        default=0.0,
        ge=-1.0,
        le=1.0,
        description=(
            "Overall sentiment score of the journal entry from -1.0 to 1.0, "
            "where -1.0 is strongly negative, 0.0 is neutral or mixed, "
            "and 1.0 is strongly positive."
        ),
    )

    tags: list[str] = Field(
        default_factory=list,
        max_length=5,
        description=(
            " Generate up to 5 concise and relevant tags based only on the journal "
            "entry. Each tag must contain between 3 and 20 characters. Reuse matching "
            "tags from 'Available existing tags' when appropriate; otherwise create "
            "new tags in the same language as the entry and in nominative form. "
            "Tags must be unique, specific, and must not contain unsupported information."
            " If the entry does not contain meaningful, interpretable content, return an empty list of tags."
        ),
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


class ResponseSchema(BaseModel):
    answer: str = Field(
        default="I am sorry but I could not make that request",
        description=(
            "The final natural-language response to the user. "
            "If tools were used, base the answer only on the returned tool results "
            "and accurately describe what was found or completed. "
            "If no tool was required, answer directly based on the user's request "
            "and the assistant's allowed general knowledge. "
            "Do not invent journal entries, completed operations, dates, tags, "
            "or other user-specific information, answer in user's native language."
        ),
    )


class VectorResult(BaseModel):
    entry: Entry
    relevance_score: float


class ToolBase(BaseModel):
    name: str
    call_id: str


class ToolData(ToolBase):
    arguments: dict


class ToolOutput(ToolBase):
    output: str
