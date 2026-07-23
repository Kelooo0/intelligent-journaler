import pytest


@pytest.mark.asyncio
async def test_register_client(client):
    response = await client.post(
        "/auth/register", json={"email": "user@example.com", "password": "password"}
    )

    assert response.status_code == 201
    assert "id" in response.json()
    assert "email" in response.json()
    assert response.json()["email"] == "user@example.com"


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post(
        "/auth/register", json={"email": "user@example.com", "password": "password"}
    )

    response = await client.post(
        "/auth/login", data={"username": "user@example.com", "password": "password"}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post(
        "/auth/register", json={"email": "user@example.com", "password": "password"}
    )

    response = await client.post(
        "/auth/login", data={"username": "user@example.com", "password": "password1"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"
