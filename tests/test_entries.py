from unittest.mock import MagicMock

import pytest
from sqlalchemy import select


@pytest.mark.asyncio
async def test_get_entries(test_entry, authorized_client):
    response = await authorized_client.get("/entries")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["id"] == 1


@pytest.mark.asyncio
async def test_get_entry(test_entry, authorized_client):
    response = await authorized_client.get(f"/entries/{test_entry.id}")

    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["id"] == test_entry.id


@pytest.mark.asyncio
async def test_create_entry(authorized_client, mock_ai):
    response = await authorized_client.post(
        "/entries",
        json={
            "content": "Today was a very good day, I woke up, went for a walk, watched my favorite series all day"
        },
    )

    assert response.status_code == 201
    assert response.json()["summary"] == "A good day"
    assert response.json()["mood"] == "happy"
    assert response.json()["sentiment_score"] == 0.9
    tag_names = [tag["name"] for tag in response.json()["tags"]]
    assert "relax" in tag_names
    assert len(tag_names) == 1


@pytest.mark.asyncio
async def test_update_entry(test_entry, authorized_client, mock_ai):
    mock_response = MagicMock()
    mock_response.summary = "A bad day"
    mock_response.mood = "angry"
    mock_response.sentiment_score = -0.9
    mock_response.tags = ["stress"]
    mock_ai.return_value = mock_response

    response = await authorized_client.patch(
        f"/entries/{test_entry.id}",
        json={
            "content": "Today was a very bad day, I woke up,"
            " went for a walk when it started to rain"
        },
    )

    assert response.status_code == 200
    assert response.json()["summary"] == "A bad day"
    assert response.json()["mood"] == "angry"
    assert response.json()["sentiment_score"] == -0.9
    tag_names = [tag["name"] for tag in response.json()["tags"]]
    assert "stress" in tag_names
    assert len(tag_names) == 1


@pytest.mark.asyncio
async def test_delete_entry(authorized_client, test_entry, db_session):
    response = await authorized_client.delete(f"/entries/{test_entry.id}")

    assert response.status_code == 204
    from app.models import EntryModel

    entry = await db_session.scalar(
        select(EntryModel).where(EntryModel.id == test_entry.id)
    )
    assert entry is None


@pytest.mark.asyncio
async def test_get_nonexistent_entry(authorized_client, db_session):
    response = await authorized_client.get("/entries/999")

    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "Entry not found"


@pytest.mark.asyncio
async def test_get_someones_entry(client, test_entry):
    await client.post(
        "/auth/register", json={"email": "user2@example.com", "password": "password"}
    )

    login_response = await client.post(
        "/auth/login", data={"username": "user2@example.com", "password": "password"}
    )
    user2_token = login_response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {user2_token}"})
    get_response = await client.get(f"/entries/{test_entry.id}")

    assert get_response.status_code == 404
    assert "detail" in get_response.json()
    assert get_response.json()["detail"] == "Entry not found"


@pytest.mark.asyncio
async def test_tags(authorized_client, test_entry):
    response = await authorized_client.get("/entries", params={"tags": "sport"})

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data == []


@pytest.mark.asyncio
async def test_date_filtering(authorized_client, test_entry):
    response = await authorized_client.get(
        "/entries", params={"start_date": "2020-01-01", "end_date": "2020-01-01"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data == []
