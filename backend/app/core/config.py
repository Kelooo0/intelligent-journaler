from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    TEST_DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"
    LOG_LEVEL: str = "INFO"
    LLM_PROVIDER: str = "mock"
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    VECTOR_TOP_K_RETRIEVAL: int = 10
    VECTOR_TOP_K_FINAL: int = 3
    VECTOR_HIGH_TRESHOLD: float = 0.80
    VECTOR_MEDIUM_TRESHOLD: float = 0.65
    VECTOR_FALLBACK_TRESHOLD: float = 0.30
    VECTOR_DELTA: float = 0.10
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 60
    FRONTEND_URL: str = "http://localhost:5173"

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        pw = quote_plus(self.DB_PASS)
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{pw}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
