import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.engine import get_session
from src.db.repositories.insight_repository import InsightRepository
from src.middleware.auth import get_current_patient_id, require_patient_match
from src.models.schemas import InsightResponse

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/patients/{patient_id}", response_model=list[InsightResponse])
async def get_patient_insights(
    patient_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),  # noqa: B008
    current_patient_id: uuid.UUID | None = Depends(get_current_patient_id),  # noqa: B008
) -> list[InsightResponse]:
    """Get AI-generated personal health insights."""
    require_patient_match(patient_id, current_patient_id)

    repo = InsightRepository(session)
    insights = await repo.get_for_patient(patient_id)
    return [
        InsightResponse(
            id=i.id,
            insight_text=i.insight_text,
            insight_type=i.insight_type,
            correlation_data=i.correlation_data,
            generated_at=i.generated_at,
        )
        for i in insights
    ]
