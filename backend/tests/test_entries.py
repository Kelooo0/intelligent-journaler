import pytest
from sqlalchemy import select


@pytest.mark.asyncio
async def test_get_entries(test_entry, authorized_client):
    response = await authorized_client.get("/entries")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["id"] == test_entry.id


@pytest.mark.asyncio
async def test_get_entry(test_entry, authorized_client):
    response = await authorized_client.get(f"/entries/{test_entry.id}")

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["id"] == test_entry.id
    assert data["user_id"] == test_entry.user_id
    assert data["content"] == test_entry.content
    tags = [tag for tag in data["tags"]]
    assert len(tags) == 3


@pytest.mark.asyncio
async def test_create_entry(authorized_client, db_session, test_user):
    response = await authorized_client.post(
        "/entries",
        json={"content": "An example of a standard entry content"},
    )

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    entry_id = data["id"]
    from app.models.models import EntryModel

    entry = await db_session.scalar(
        select(EntryModel).where(EntryModel.user_id == test_user.id, EntryModel.id == entry_id)
    )
    assert entry
    assert data["id"] == entry.id
    assert data["user_id"] == entry.user_id
    assert data["content"] == entry.content
    tags = [tag for tag in data["tags"]]
    assert len(tags) == 3


@pytest.mark.asyncio
async def test_update_entry(test_entry, authorized_client):

    response = await authorized_client.patch(
        f"/entries/{test_entry.id}",
        json={"content": "An example of an updated entry content"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["id"] == test_entry.id
    assert data["user_id"] == test_entry.user_id
    assert data["content"] == "An example of an updated entry content"
    tags = [tag for tag in data["tags"]]
    assert len(tags) == 3


@pytest.mark.asyncio
async def test_delete_entry(authorized_client, test_entry, test_user, db_session):
    response = await authorized_client.delete(f"/entries/{test_entry.id}")

    assert response.status_code == 204
    from app.models.models import EntryModel

    entry = await db_session.scalar(
        select(EntryModel).where(EntryModel.user_id == test_user.id, EntryModel.id == test_entry.id)
    )
    assert entry is None


@pytest.mark.asyncio
async def test_get_nonexistent_entry(authorized_client):
    response = await authorized_client.get("/entries/999")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Entry not found"


@pytest.mark.asyncio
async def test_get_someones_entry(client, test_entry):
    await client.post("/auth/register", json={"email": "user2@example.com", "password": "password"})

    login_response = await client.post(
        "/auth/login", data={"username": "user2@example.com", "password": "password"}
    )
    user2_token = login_response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {user2_token}"})
    get_response = await client.get(f"/entries/{test_entry.id}")

    assert get_response.status_code == 404
    data = get_response.json()
    assert "detail" in data
    assert data["detail"] == "Entry not found"


@pytest.mark.asyncio
async def test_tags(authorized_client, test_entry):
    response = await authorized_client.get("/entries", params={"tags": "sport"})

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data == []  # No entries have 'sport' tag, so search returns an empty list


@pytest.mark.asyncio
async def test_date_filtering(authorized_client, test_entry):
    response = await authorized_client.get(
        "/entries", params={"start_date": "2020-01-01", "end_date": "2020-01-01"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data == []  # No entries exist for 2020-01-01, expect empty result
