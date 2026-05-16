def test_register_client(client):
    response = client.post(
        "/auth/register", json={"email": "user@example.com", "password": "password"}
    )

    assert response.status_code == 201
    assert "id" and "email" in response.json()
    assert response.json()["email"] == "user@example.com"


def test_login_success(client, db_session):
    client.post(
        "/auth/register", json={"email": "user@example.com", "password": "password"}
    )

    response = client.post(
        "/auth/login", data={"username": "user@example.com", "password": "password"}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client, db_session):
    client.post(
        "/auth/register", json={"email": "user@example.com", "password": "password"}
    )

    response = client.post(
        "/auth/login", data={"username": "user@example.com", "password": "password1"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"
