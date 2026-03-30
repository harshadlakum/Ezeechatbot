import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_chat_invalid_bot():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/chat", json={
            "bot_id": "nonexistent-bot-id-0000",
            "user_message": "What is the leave policy?",
            "conversation_history": [],
        })
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_stats_invalid_bot():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/stats/nonexistent-bot-id-0000")
    assert response.status_code == 404
