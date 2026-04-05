import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.engine import get_session
from src.middleware.auth import get_current_patient_id, require_patient_match
from src.models.habit_templates import HABIT_TEMPLATES
from src.models.schemas import ActivateHabitRequest, HabitResponse
from src.services.habit_service import HabitService

router = APIRouter(prefix="/habits", tags=["habits"])


@router.get("/templates")
async def get_habit_templates() -> list[dict[str, str]]:
    """Return all available habit templates grouped by dimension."""
    return [
        {
            "id": t.id,
            "name": t.name,
            "dimension": t.dimension,
            "description": t.description_fr,
        }
        for t in HABIT_TEMPLATES.values()
    ]


def _get_habit_service(
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> HabitService:
    """Provide a HabitService instance."""
    return HabitService(session)


@router.post("/activate", status_code=201, response_model=HabitResponse)
async def activate_habit(
    request: ActivateHabitRequest,
    service: HabitService = Depends(_get_habit_service),  # noqa: B008
    current_patient_id: uuid.UUID | None = Depends(get_current_patient_id),  # noqa: B008
) -> HabitResponse:
    """Activate a new micro-habit from the template library."""
    require_patient_match(request.patient_id, current_patient_id)

    try:
        habit = await service.activate_habit(
            patient_id=request.patient_id,
            template_id=request.template_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return HabitResponse(
        id=habit.id,
        patient_id=habit.patient_id,
        template_id=habit.template_id,
        name=habit.name,
        dimension=habit.dimension,
        started_at=habit.started_at,
        is_active=habit.is_active,
        current_streak=0,
        completed_today=False,
    )


@router.post("/{habit_id}/complete", status_code=201)
async def complete_habit(
    habit_id: uuid.UUID,
    service: HabitService = Depends(_get_habit_service),  # noqa: B008
    current_patient_id: uuid.UUID | None = Depends(get_current_patient_id),  # noqa: B008
) -> dict[str, str]:
    """Mark a habit as completed for today."""
    try:
        await service.complete_habit(habit_id, current_patient_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"status": "completed", "message": "Bravo ! Habitude completee."}


@router.get("/patients/{patient_id}", response_model=list[HabitResponse])
async def get_patient_habits(
    patient_id: uuid.UUID,
    service: HabitService = Depends(_get_habit_service),  # noqa: B008
    current_patient_id: uuid.UUID | None = Depends(get_current_patient_id),  # noqa: B008
) -> list[HabitResponse]:
    """Get active habits with streak information."""
    require_patient_match(patient_id, current_patient_id)

    habits_data = await service.get_active_habits_with_streaks(patient_id)
    return [
        HabitResponse(**h)  # type: ignore[arg-type]
        for h in habits_data
    ]
