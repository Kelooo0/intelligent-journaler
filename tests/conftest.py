import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.database import Base
from app.core.dependencies import get_ai, get_db, get_vector
from app.main import app

engine = create_async_engine(
    settings.TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(autouse=True)
async def use_mock(monkeypatch):
    monkeypatch.setattr(settings, "LLM_PROVIDER", "mock")


@pytest_asyncio.fixture
async def ai_service():
    return get_ai()


@pytest_asyncio.fixture
async def vector_service():
    return get_vector()


@pytest_asyncio.fixture
async def client(db_session, ai_service, vector_service):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async def override_get_ai():
        yield ai_service

    app.dependency_overrides[get_ai] = override_get_ai

    async def override_get_vector():
        yield vector_service

    app.dependency_overrides[get_vector] = override_get_vector

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def authorized_client(client, db_session):
    await client.post(
        "/auth/register", json={"email": "user@example.com", "password": "password"}
    )

    response = await client.post(
        "/auth/login", data={"username": "user@example.com", "password": "password"}
    )
    access_token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client


@pytest_asyncio.fixture
async def test_user(authorized_client, db_session):
    from app.models.models import UserModel

    return await db_session.scalar(
        select(UserModel).where(UserModel.email == "user@example.com")
    )


@pytest_asyncio.fixture
async def test_entry(db_session, test_user, ai_service):
    from app.schemas.schemas import EntryCreate
    from app.services.entries_service import create_entry_service

    entry_in = EntryCreate(
        content="Today was a very good day, I woke up, went for a walk,"
        " watched my favorite series all day"
    )

    return await create_entry_service(entry_in, db_session, test_user, ai_service)
