import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.meal_analyzer import MealAnalyzer
from src.config.settings import settings
from src.db.engine import get_session
from src.db.repositories.meal_repository import MealRepository
from src.middleware.auth import get_current_patient_id, require_patient_match
from src.models.schemas import MealAnalyzeRequest, MealResponse
from src.services.meal_service import MealService

router = APIRouter(prefix="/meals", tags=["meals"])


def _get_meal_service(
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> MealService:
    """Provide a MealService instance."""
    analyzer = None
    if settings.mistral_api_key:
        analyzer = MealAnalyzer(settings.mistral_api_key, session)
    return MealService(analyzer, session)


@router.post("/analyze", status_code=201, response_model=MealResponse)
async def analyze_meal(
    request: MealAnalyzeRequest,
    service: MealService = Depends(_get_meal_service),  # noqa: B008
    current_patient_id: uuid.UUID | None = Depends(get_current_patient_id),  # noqa: B008
) -> MealResponse:
    """Analyze a meal photo with AI and return nutritional assessment."""
    require_patient_match(request.patient_id, current_patient_id)

    try:
        meal = await service.analyze_and_store(
            patient_id=request.patient_id,
            image_base64=request.image_base64,
            meal_type=request.meal_type.value,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return MealResponse(
        id=meal.id,
        patient_id=meal.patient_id,
        photo_url=meal.photo_url,
        analysis=meal.analysis,
        nutrition_score=meal.nutrition_score,
        meal_type=meal.meal_type,
        date=meal.date,
        created_at=meal.created_at,
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
