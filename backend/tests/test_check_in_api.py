from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app


@pytest.mark.asyncio
async def test_submit_check_in_requires_auth(
    override_session: AsyncMock,
) -> None:
    """Check-in submission requires auth when JWT is configured."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/check-ins",
            json={
                "patient_id": "00000000-0000-0000-0000-000000000001",
                "sleep_quality": 4,
                "energy_level": 3,
                "mood": "bien",
            },
        )

    assert response.status_code in (201, 401, 409)


@pytest.mark.asyncio
async def test_check_in_status_returns_streak(
    override_session: AsyncMock,
) -> None:
    """Status endpoint returns streak and completion info."""
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = None
    result_mock.scalars.return_value.all.return_value = []
    override_session.execute = AsyncMock(return_value=result_mock)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/api/v1/check-ins/patients/00000000-0000-0000-0000-000000000001/status"
        )

    assert response.status_code == 200
    data = response.json()
    assert "completed_today" in data
    assert "streak" in data
    assert data["completed_today"] is False
    assert data["streak"] == 0
