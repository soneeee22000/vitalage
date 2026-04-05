import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.check_in_analyzer import CheckInAnalyzer
from src.config.settings import settings
from src.db.engine import get_session
from src.middleware.auth import get_current_patient_id, require_patient_match
from src.models.schemas import (
    CheckInRequest,
    CheckInResponse,
    CheckInStatusResponse,
)
from src.services.check_in_service import CheckInService
from src.services.vitality_service import VitalityService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/check-ins", tags=["check-ins"])


def _get_check_in_service(
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> CheckInService:
    """Provide a CheckInService instance."""
    analyzer = None
    if settings.mistral_api_key:
        analyzer = CheckInAnalyzer(settings.mistral_api_key, session)
    return CheckInService(analyzer, session)


@router.post("", status_code=201, response_model=CheckInResponse)
async def submit_check_in(
    request: CheckInRequest,
    session: AsyncSession = Depends(get_session),  # noqa: B008
    service: CheckInService = Depends(_get_check_in_service),  # noqa: B008
    current_patient_id: uuid.UUID | None = Depends(get_current_patient_id),  # noqa: B008
) -> CheckInResponse:
    """Submit a daily vitality check-in."""
    require_patient_match(request.patient_id, current_patient_id)

    try:
        check_in = await service.submit_check_in(
            patient_id=request.patient_id,
            sleep_quality=request.sleep_quality,
            energy_level=request.energy_level,
            mood=request.mood.value,
            symptoms=request.symptoms,
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    try:
        vitality_svc = VitalityService(session)
        await vitality_svc.recalculate(request.patient_id)
    except Exception:
        logger.exception("Vitality recalculation failed after check-in")

    return CheckInResponse(
        id=check_in.id,
        patient_id=check_in.patient_id,
        sleep_quality=check_in.sleep_quality,
        energy_level=check_in.energy_level,
        mood=check_in.mood,
        symptoms=check_in.symptoms,
        symptoms_structured=check_in.symptoms_structured,
        date=check_in.date,
        created_at=check_in.created_at,
    )


@router.get(
    "/patients/{patient_id}/status",
    response_model=CheckInStatusResponse,
)
async def get_check_in_status(
    patient_id: uuid.UUID,
    service: CheckInService = Depends(_get_check_in_service),  # noqa: B008
    current_patient_id: uuid.UUID | None = Depends(get_current_patient_id),  # noqa: B008
) -> CheckInStatusResponse:
    """Get today's check-in status and current streak."""
    require_patient_match(patient_id, current_patient_id)

    today_ci = await service.get_today(patient_id)
    streak = await service.get_streak(patient_id)

    today_response = None
    if today_ci:
        today_response = CheckInResponse(
            id=today_ci.id,
            patient_id=today_ci.patient_id,
            sleep_quality=today_ci.sleep_quality,
            energy_level=today_ci.energy_level,
            mood=today_ci.mood,
            symptoms=today_ci.symptoms,
            symptoms_structured=today_ci.symptoms_structured,
            date=today_ci.date,
            created_at=today_ci.created_at,
        )

    return CheckInStatusResponse(
        completed_today=today_ci is not None,
        streak=streak,
        today_check_in=today_response,
    )


@router.get("/patients/{patient_id}", response_model=list[CheckInResponse])
async def get_check_in_history(
    patient_id: uuid.UUID,
    service: CheckInService = Depends(_get_check_in_service),  # noqa: B008
    current_patient_id: uuid.UUID | None = Depends(get_current_patient_id),  # noqa: B008
) -> list[CheckInResponse]:
    """Get check-in history for a patient."""
    require_patient_match(patient_id, current_patient_id)

    check_ins = await service.get_history(patient_id)
    return [
        CheckInResponse(
            id=ci.id,
            patient_id=ci.patient_id,
            sleep_quality=ci.sleep_quality,
            energy_level=ci.energy_level,
            mood=ci.mood,
            symptoms=ci.symptoms,
            symptoms_structured=ci.symptoms_structured,
            date=ci.date,
            created_at=ci.created_at,
        )
        for ci in check_ins
    ]
