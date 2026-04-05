import uuid
from datetime import date, datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.check_in_analyzer import CheckInAnalyzer
from src.db.repositories.check_in_repository import CheckInRepository
from src.db.tables import CheckInTable


class CheckInService:
    """Service for managing daily health check-ins."""

    def __init__(
        self,
        analyzer: CheckInAnalyzer | None,
        session: AsyncSession,
    ) -> None:
        self._analyzer = analyzer
        self._repo = CheckInRepository(session)
        self._session = session

    async def submit_check_in(
        self,
        patient_id: uuid.UUID,
        sleep_quality: int,
        energy_level: int,
        mood: str,
        symptoms: str | None = None,
    ) -> CheckInTable:
        """Submit a daily check-in. One per patient per day."""
        today = date.today()
        existing = await self._repo.get_by_patient_and_date(patient_id, today)
        if existing:
            raise ValueError("Vous avez deja complete votre bilan aujourd'hui")

        symptoms_structured = None
        if symptoms and self._analyzer:
            patient_ref = f"Patient/{patient_id}"
            symptoms_structured = await self._analyzer.analyze_symptoms(
                symptoms, patient_ref
            )

        row = CheckInTable(
            patient_id=patient_id,
            sleep_quality=sleep_quality,
            energy_level=energy_level,
            mood=mood,
            symptoms=symptoms,
            symptoms_structured=symptoms_structured,
            date=today,
            created_at=datetime.now(tz=timezone.utc),
        )

        created = await self._repo.create(row)
        await self._session.commit()
        return created

    async def get_history(
        self, patient_id: uuid.UUID, limit: int = 30
    ) -> list[CheckInTable]:
        """Get check-in history for a patient."""
        return await self._repo.get_recent(patient_id, limit)

    async def get_today(
        self, patient_id: uuid.UUID
    ) -> CheckInTable | None:
        """Check if today's check-in exists."""
        return await self._repo.get_by_patient_and_date(patient_id, date.today())

    async def get_streak(self, patient_id: uuid.UUID) -> int:
        """Calculate consecutive check-in days ending today or yesterday."""
        check_ins = await self._repo.get_recent(patient_id, limit=60)
        if not check_ins:
            return 0

        check_in_dates = sorted(
            {ci.date for ci in check_ins}, reverse=True
        )

        today = date.today()
        streak = 0
        expected = today

        for d in check_in_dates:
            if d == expected:
                streak += 1
                expected -= timedelta(days=1)
            elif d == today - timedelta(days=1) and expected == today:
                expected = d
                streak += 1
                expected -= timedelta(days=1)
            else:
                break

        return streak
