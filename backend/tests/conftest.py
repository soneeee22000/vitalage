import uuid
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.engine import get_session
from src.main import app


@pytest.fixture
def mock_session() -> AsyncMock:
    """Provide a mock AsyncSession with common operations stubbed."""
    session = AsyncMock(spec=AsyncSession)
    session.commit = AsyncMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    session.add = MagicMock()
    session.get = AsyncMock(return_value=None)
    session.execute = AsyncMock()
    return session


@pytest.fixture
def patient_id() -> uuid.UUID:
    """Provide a deterministic test patient UUID."""
    return uuid.UUID("00000000-0000-0000-0000-000000000001")


@pytest.fixture
def sample_patient_fhir(patient_id: uuid.UUID) -> dict[str, Any]:
    """Provide a sample FHIR Patient resource."""
    return {
        "resourceType": "Patient",
        "id": str(patient_id),
        "identifier": [
            {"system": "https://vitalage.health/fhir", "value": "VA-TEST001"}
        ],
        "name": [{"given": ["Marie"], "family": "Dupont"}],
    }


@pytest.fixture
def override_session(mock_session: AsyncMock) -> AsyncMock:
    """Override the get_session dependency with a mock session."""
    async def _override() -> AsyncSession:  # type: ignore[misc]
        return mock_session  # type: ignore[return-value]

    app.dependency_overrides[get_session] = _override
    yield mock_session
    app.dependency_overrides.clear()


@pytest.fixture
def async_client() -> ASGITransport:
    """Provide an ASGI transport for the test app."""
    return ASGITransport(app=app)


def mock_mistral_chat_response(content: str) -> MagicMock:
    """Create a mock Mistral chat.complete_async response."""
    message = MagicMock()
    message.content = content
    choice = MagicMock()
    choice.message = message
    response = MagicMock()
    response.choices = [choice]
    return response
