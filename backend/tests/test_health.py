from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app


@pytest.mark.asyncio
async def test_health_check_returns_ok(override_session: AsyncMock) -> None:
    """Health endpoint returns healthy status."""
    result_mock = MagicMock()
    override_session.execute = AsyncMock(return_value=result_mock)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "vitalage-api"


@pytest.mark.asyncio
async def test_health_check_db_unhealthy(override_session: AsyncMock) -> None:
    """Health endpoint returns degraded when DB is unreachable."""
    override_session.execute = AsyncMock(side_effect=Exception("Connection refused"))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "degraded"
    assert data["database"] == "unhealthy"
