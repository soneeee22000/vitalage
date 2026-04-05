import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.engine import get_session
from src.db.repositories.meal_repository import MealRepository
from src.middleware.auth import get_current_patient_id, require_patient_match
from src.models.schemas import MealAnalyzeRequest, MealResponse

router = APIRouter(prefix="/meals", tags=["meals"])


@router.post("/analyze", status_code=201, response_model=MealResponse)
async def analyze_meal(
    request: MealAnalyzeRequest,
    session: AsyncSession = Depends(get_session),  # noqa: B008
    current_patient_id: uuid.UUID | None = Depends(get_current_patient_id),  # noqa: B008
) -> MealResponse:
    """Analyze a meal photo with AI and return nutritional assessment."""
    require_patient_match(request.patient_id, current_patient_id)

    raise HTTPException(
        status_code=501,
        detail="Analyse de repas en cours de developpement. Disponible bientot.",
    )


@router.get("/patients/{patient_id}", response_model=list[MealResponse])
async def get_meal_history(
    patient_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),  # noqa: B008
    current_patient_id: uuid.UUID | None = Depends(get_current_patient_id),  # noqa: B008
) -> list[MealResponse]:
    """Get meal analysis history for a patient."""
    require_patient_match(patient_id, current_patient_id)

    repo = MealRepository(session)
    meals = await repo.get_recent(patient_id)
    return [
        MealResponse(
            id=m.id,
            patient_id=m.patient_id,
            photo_url=m.photo_url,
            analysis=m.analysis,
            nutrition_score=m.nutrition_score,
            meal_type=m.meal_type,
            date=m.date,
            created_at=m.created_at,
        )
        for m in meals
    ]
