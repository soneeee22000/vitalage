import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.base_repository import BaseRepository
from src.db.tables import MealTable


class MealRepository(BaseRepository[MealTable]):
    """Repository for meal analysis records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(MealTable, session)

    async def get_recent(
        self, patient_id: uuid.UUID, limit: int = 7
    ) -> list[MealTable]:
        """Get recent meals ordered by date descending."""
        stmt = (
            select(MealTable)
            .where(MealTable.patient_id == patient_id)
            .order_by(MealTable.date.desc())
            .limit(limit * 4)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
