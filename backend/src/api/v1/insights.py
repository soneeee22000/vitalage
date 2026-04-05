import logging
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.insight_engine import InsightEngine
from src.config.settings import settings
from src.db.engine import get_session
from src.middleware.auth import get_current_patient_id, require_patient_match
from src.models.schemas import InsightResponse
from src.services.insight_service import InsightService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/insights", tags=["insights"])


def _get_insight_service(
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> InsightService:
    """Provide an InsightService instance."""
    engine = None
    if settings.mistral_api_key:
        engine = InsightEngine(settings.mistral_api_key, session)
    return InsightService(engine, session)


@router.get("/patients/{patient_id}", response_model=list[InsightResponse])
async def get_patient_insights(
    patient_id: uuid.UUID,
    service: InsightService = Depends(_get_insight_service),  # noqa: B008
    current_patient_id: uuid.UUID | None = Depends(get_current_patient_id),  # noqa: B008
) -> list[InsightResponse]:
    """Get AI-generated personal health insights."""
    require_patient_match(patient_id, current_patient_id)

    insights = await service.get_insights(patient_id)

    if not insights:
        try:
            generated = await service.generate_if_ready(patient_id)
            if generated:
                insights = generated
        except Exception:
            logger.exception("Insight generation failed")

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
