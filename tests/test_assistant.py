import pytest


@pytest.mark.asyncio
async def test_assistant_response(authorized_client):
    response = await authorized_client.post(
        "/assistant", json={"content": "An example user query"}
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert response.text == "This is a mock assistant response"
