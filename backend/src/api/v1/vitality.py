import uuid
from datetime import timedelta
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.engine import get_session
from src.db.repositories.vitality_repository import VitalityScoreRepository
from src.middleware.auth import get_current_patient_id, require_patient_match
from src.models.schemas import (
    VitalityScoreResponse,
    VitalityTrendPoint,
    VitalityTrendResponse,
)

router = APIRouter(prefix="/vitality", tags=["vitality"])


@router.get("/patients/{patient_id}", response_model=VitalityScoreResponse)
async def get_vitality_score(
    patient_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),  # noqa: B008
    current_patient_id: uuid.UUID | None = Depends(get_current_patient_id),  # noqa: B008
) -> VitalityScoreResponse:
    """Get the current vitality score with dimension breakdown."""
    require_patient_match(patient_id, current_patient_id)

    repo = VitalityScoreRepository(session)
    latest = await repo.get_latest(patient_id)
    if latest is None:
        raise HTTPException(
            status_code=404,
            detail="Pas encore de score de vitalite. Continuez vos bilans quotidiens.",
        )

    history = await repo.get_history(patient_id, limit=30)
    change = None
    if len(history) >= 2:
        now = latest.calculated_at
        week_ago = now - timedelta(days=7)
        older_scores = [
            s for s in history
            if s.id != latest.id and s.calculated_at <= week_ago
        ]
        if older_scores:
            change = latest.overall - older_scores[0].overall

    return VitalityScoreResponse(
        patient_id=latest.patient_id,
        nutrition=latest.nutrition,
        sleep=latest.sleep,
        activity=latest.activity,
        mood=latest.mood,
        overall=latest.overall,
        calculated_at=latest.calculated_at,
        change_from_last_week=change,
    )


@router.get(
    "/patients/{patient_id}/trends",
    response_model=VitalityTrendResponse,
)
async def get_vitality_trends(
    patient_id: uuid.UUID,
    period: Literal["7d", "30d"] = "7d",
    session: AsyncSession = Depends(get_session),  # noqa: B008
    current_patient_id: uuid.UUID | None = Depends(get_current_patient_id),  # noqa: B008
) -> VitalityTrendResponse:
    """Get vitality score trends over time."""
    require_patient_match(patient_id, current_patient_id)

    limit = 7 if period == "7d" else 30
    repo = VitalityScoreRepository(session)
    scores = await repo.get_history(patient_id, limit=limit)

    data = [
        VitalityTrendPoint(
            date=s.calculated_at.date(),
            overall=s.overall,
            nutrition=s.nutrition,
            sleep=s.sleep,
            activity=s.activity,
            mood=s.mood,
        )
        for s in reversed(scores)
    ]

    return VitalityTrendResponse(
        patient_id=patient_id,
        period=period,
        data=data,
    )
