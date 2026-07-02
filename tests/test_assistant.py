import pytest


@pytest.mark.asyncio
async def test_assistant_response(authorized_client):
    response = await authorized_client.post(
        "/assistant", json={"content": "An example user query"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["answer"] == "Example AI assistent response"
    used_entries = [e for e in data["used_entries"]]
    assert len(used_entries) == 3
    assert data["intent"] == "emotional_reflection"
