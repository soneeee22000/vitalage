from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app


@pytest.mark.asyncio
async def test_get_templates_returns_list(
    override_session: AsyncMock,
) -> None:
    """Templates endpoint returns available habit templates."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/habits/templates")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 12
    first = data[0]
    assert "id" in first
    assert "name" in first
    assert "dimension" in first
    assert "description" in first


@pytest.mark.asyncio
async def test_templates_cover_all_dimensions(
    override_session: AsyncMock,
) -> None:
    """Templates include all 4 vitality dimensions."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/habits/templates")

    data = response.json()
    dimensions = {t["dimension"] for t in data}
    assert dimensions == {"sleep", "nutrition", "activity", "mood"}


@pytest.mark.asyncio
async def test_get_habits_empty(override_session: AsyncMock) -> None:
    """Patient with no habits gets empty list."""
    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = []
    override_session.execute = AsyncMock(return_value=result_mock)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/api/v1/habits/patients/00000000-0000-0000-0000-000000000001"
        )

    assert response.status_code == 200
    assert response.json() == []
