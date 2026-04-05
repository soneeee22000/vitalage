import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.base_repository import BaseRepository
from src.db.tables import InsightTable


class InsightRepository(BaseRepository[InsightTable]):
    """Repository for AI-generated insight records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(InsightTable, session)

    async def get_for_patient(
        self, patient_id: uuid.UUID, limit: int = 10
    ) -> list[InsightTable]:
        """Get insights for a patient ordered by most recent."""
        stmt = (
            select(InsightTable)
            .where(InsightTable.patient_id == patient_id)
            .order_by(InsightTable.generated_at.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
