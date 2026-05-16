import pytest
from app.config import settings
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app
from app.database import get_db
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

engine = create_engine(
    settings.TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)

    connection = engine.connect()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    connection.close()

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def test_user_token(client, db_session):
    client.post(
        "/auth/register", json={"email": "user@example.com", "password": "password"}
    )

    response = client.post(
        "/auth/login", data={"username": "user@example.com", "password": "password"}
    )
    return response.json()["access_token"]


@pytest.fixture
def test_user(test_user_token, db_session):
    from app.models import UserModel

    return (
        db_session.query(UserModel)
        .filter(UserModel.email == "user@example.com")
        .first()
    )


@pytest.fixture
def authorized_client(client, test_user_token):
    client.headers.update({"Authorization": f"Bearer {test_user_token}"})
    return client


@pytest.fixture
def test_entry(db_session, test_user):
    from app.schemas import EntryCreate
    from app.services.entries_service import create_entry_service

    entry_in = EntryCreate(
        content="Today was a very good day, I woke up, went for a walk, watched my favorite series all day"
    )
    with patch("app.services.entries_service.ai_service.analyze_entry") as mock_ai:
        mock_response = MagicMock()
        mock_response.summary = "A good day"
        mock_response.mood = "happy"
        mock_response.sentiment_score = 0.9
        mock_response.tags = ["relax"]
        mock_ai.return_value = mock_response

        return create_entry_service(entry_in, db_session, test_user)
