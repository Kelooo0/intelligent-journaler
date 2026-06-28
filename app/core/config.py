from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    GEMINI_API_KEY: str
    TEST_DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"
    LOG_LEVEL: str = "INFO"
    LLM_PROVIDER: str = "gemini"
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_MODEL_LITE: str = "gemini-2.5-flash-lite"
    GEMINI_EMBEDDING_MODEL: str = "gemini-embedding-001"
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        pw = quote_plus(self.DB_PASS)
        return f"postgresql+asyncpg://{self.DB_USER}:{pw}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
