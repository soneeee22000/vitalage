import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.base_repository import BaseRepository
from src.db.tables import VitalityScoreTable


class VitalityScoreRepository(BaseRepository[VitalityScoreTable]):
    """Repository for vitality score snapshots."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(VitalityScoreTable, session)

    async def get_latest(
        self, patient_id: uuid.UUID
    ) -> VitalityScoreTable | None:
        """Get the most recent vitality score for a patient."""
        stmt = (
            select(VitalityScoreTable)
            .where(VitalityScoreTable.patient_id == patient_id)
            .order_by(VitalityScoreTable.calculated_at.desc())
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_history(
        self, patient_id: uuid.UUID, limit: int = 30
    ) -> list[VitalityScoreTable]:
        """Get vitality score history ordered by date."""
        stmt = (
            select(VitalityScoreTable)
            .where(VitalityScoreTable.patient_id == patient_id)
            .order_by(VitalityScoreTable.calculated_at.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
