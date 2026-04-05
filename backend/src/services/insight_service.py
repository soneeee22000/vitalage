import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.insight_engine import InsightEngine
from src.db.repositories.check_in_repository import CheckInRepository
from src.db.repositories.insight_repository import InsightRepository
from src.db.tables import CheckInTable, InsightTable

MIN_DAYS_FOR_INSIGHTS = 7


class InsightService:
    """Service for generating and managing personal health insights."""

    def __init__(
        self, engine: InsightEngine | None, session: AsyncSession
    ) -> None:
        self._engine = engine
        self._check_in_repo = CheckInRepository(session)
        self._insight_repo = InsightRepository(session)
        self._session = session

    async def get_insights(
        self, patient_id: uuid.UUID
    ) -> list[InsightTable]:
        """Get existing insights for a patient."""
        return await self._insight_repo.get_for_patient(patient_id)

    async def generate_if_ready(
        self, patient_id: uuid.UUID
    ) -> list[InsightTable] | None:
        """Generate insights if enough data exists. Returns None if not ready."""
        if not self._engine:
            return None

        check_ins = await self._check_in_repo.get_recent(
            patient_id, limit=30
        )
        if len(check_ins) < MIN_DAYS_FOR_INSIGHTS:
            return None

        data_summary = self._build_data_summary(check_ins)
        patient_ref = f"Patient/{patient_id}"

        raw_insights = await self._engine.generate_insights(
            data_summary, patient_ref
        )

        created_insights: list[InsightTable] = []
        now = datetime.now(tz=timezone.utc)

        for insight_data in raw_insights[:5]:
            text = insight_data.get("text", "")
            insight_type = insight_data.get("type", "correlation")
            correlation_data = insight_data.get("data", {})

            if not text:
                continue

            row = InsightTable(
                patient_id=patient_id,
                insight_text=text,
                insight_type=insight_type,
                correlation_data=correlation_data,
                generated_at=now,
            )
            created = await self._insight_repo.create(row)
            created_insights.append(created)

        await self._session.commit()
        return created_insights

    @staticmethod
    def _build_data_summary(check_ins: list[CheckInTable]) -> str:
        """Build a text summary of check-in data for the AI."""
        lines = []
        for ci in reversed(check_ins):
            symptoms_text = f", symptomes: {ci.symptoms}" if ci.symptoms else ""
            lines.append(
                f"{ci.date}: sommeil={ci.sleep_quality}/5, "
                f"energie={ci.energy_level}/5, humeur={ci.mood}"
                f"{symptoms_text}"
            )
        return "\n".join(lines)
