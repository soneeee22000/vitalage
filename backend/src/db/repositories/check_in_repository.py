import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.base_repository import BaseRepository
from src.db.tables import CheckInTable


class CheckInRepository(BaseRepository[CheckInTable]):
    """Repository for daily check-in records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(CheckInTable, session)

    async def get_by_patient_and_date(
        self, patient_id: uuid.UUID, check_date: date
    ) -> CheckInTable | None:
        """Find a check-in for a specific patient and date."""
        stmt = select(CheckInTable).where(
            CheckInTable.patient_id == patient_id,
            CheckInTable.date == check_date,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_recent(
        self, patient_id: uuid.UUID, limit: int = 7
    ) -> list[CheckInTable]:
        """Get recent check-ins ordered by date descending."""
        stmt = (
            select(CheckInTable)
            .where(CheckInTable.patient_id == patient_id)
            .order_by(CheckInTable.date.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
