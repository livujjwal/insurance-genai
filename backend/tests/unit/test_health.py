from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient

from app.api.deps import get_db, get_redis


@pytest.mark.asyncio
async def test_root_endpoint(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "health" in data


@pytest.mark.asyncio
async def test_health_endpoint_mocked(async_client: AsyncClient):
    # Mock DB and Redis dependencies
    mock_db = AsyncMock()
    mock_db.execute = AsyncMock()

    mock_redis = AsyncMock()
    mock_redis.ping = AsyncMock(return_value=True)

    from app.main import app

    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_redis] = lambda: mock_redis

    try:
        response = await async_client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["services"]["database"] == "healthy"
        assert data["services"]["redis"] == "healthy"
    finally:
        app.dependency_overrides.clear()
