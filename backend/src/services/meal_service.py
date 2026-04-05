import uuid
from datetime import date, datetime, timezone
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.meal_analyzer import MealAnalyzer
from src.db.repositories.meal_repository import MealRepository
from src.db.tables import MealTable


class MealService:
    """Service for managing meal photo analysis."""

    def __init__(
        self, analyzer: MealAnalyzer | None, session: AsyncSession
    ) -> None:
        self._analyzer = analyzer
        self._repo = MealRepository(session)
        self._session = session

    async def analyze_and_store(
        self,
        patient_id: uuid.UUID,
        image_base64: str,
        meal_type: str,
    ) -> MealTable:
        """Analyze a meal photo and store the result."""
        analysis: dict[str, Any] = {
            "foods_identified": [],
            "nutritional_highlights": [],
            "quality_score": 50,
            "micro_tip": "Continuez a varier vos repas !",
            "summary": "Repas non analyse",
        }
        quality_score = 50

        if self._analyzer:
            patient_ref = f"Patient/{patient_id}"
            analysis = await self._analyzer.analyze_meal(
                image_base64, patient_ref
            )
            quality_score = analysis.get("quality_score", 50)

        photo_url = f"checkin://{patient_id}/{date.today().isoformat()}/{meal_type}"

        row = MealTable(
            patient_id=patient_id,
            photo_url=photo_url,
            analysis=analysis,
            nutrition_score=quality_score,
            meal_type=meal_type,
            date=date.today(),
            created_at=datetime.now(tz=timezone.utc),
        )

        created = await self._repo.create(row)
        await self._session.commit()
        return created

    async def get_history(
        self, patient_id: uuid.UUID, limit: int = 20
    ) -> list[MealTable]:
        """Get meal history for a patient."""
        return await self._repo.get_recent(patient_id, limit=limit)
