import uuid
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.base_repository import BaseRepository
from src.db.tables import HabitCompletionTable, HabitTable


class HabitRepository(BaseRepository[HabitTable]):
    """Repository for habit records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(HabitTable, session)

    async def get_active_habits(
        self, patient_id: uuid.UUID
    ) -> list[HabitTable]:
        """Get all active habits for a patient."""
        stmt = (
            select(HabitTable)
            .where(
                HabitTable.patient_id == patient_id,
                HabitTable.is_active.is_(True),
            )
            .order_by(HabitTable.started_at)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def count_active(self, patient_id: uuid.UUID) -> int:
        """Count active habits for a patient."""
        stmt = (
            select(func.count())
            .select_from(HabitTable)
            .where(
                HabitTable.patient_id == patient_id,
                HabitTable.is_active.is_(True),
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()


class HabitCompletionRepository(BaseRepository[HabitCompletionTable]):
    """Repository for habit completion records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(HabitCompletionTable, session)

    async def get_by_habit_and_date(
        self, habit_id: uuid.UUID, completed_date: date
    ) -> HabitCompletionTable | None:
        """Check if a habit was completed on a specific date."""
        stmt = select(HabitCompletionTable).where(
            HabitCompletionTable.habit_id == habit_id,
            HabitCompletionTable.completed_date == completed_date,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_completions_for_habit(
        self, habit_id: uuid.UUID, limit: int = 30
    ) -> list[HabitCompletionTable]:
        """Get recent completions for a habit."""
        stmt = (
            select(HabitCompletionTable)
            .where(HabitCompletionTable.habit_id == habit_id)
            .order_by(HabitCompletionTable.completed_date.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
