from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.check_in_analyzer import CheckInAnalyzer
from src.config.settings import settings
from src.db.engine import get_session
from src.services.audit_service import AuditService
from src.services.check_in_service import CheckInService
from src.services.consent_service import ConsentService
from src.services.habit_service import HabitService


def get_consent_service(
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> ConsentService:
    """Provide a ConsentService instance."""
    return ConsentService(session)


def get_audit_service(
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> AuditService:
    """Provide an AuditService instance."""
    return AuditService(session)


def get_check_in_service(
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> CheckInService:
    """Provide a CheckInService instance."""
    analyzer = None
    if settings.mistral_api_key:
        analyzer = CheckInAnalyzer(settings.mistral_api_key, session)
    return CheckInService(analyzer, session)


def get_habit_service(
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> HabitService:
    """Provide a HabitService instance."""
    return HabitService(session)
