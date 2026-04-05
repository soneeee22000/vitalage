import uuid
from datetime import date, datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.habit_repository import (
    HabitCompletionRepository,
    HabitRepository,
)
from src.db.tables import HabitCompletionTable, HabitTable
from src.models.habit_templates import HABIT_TEMPLATES

MAX_ACTIVE_HABITS = 3


class HabitService:
    """Service for managing micro-habits and streaks."""

    def __init__(self, session: AsyncSession) -> None:
        self._habit_repo = HabitRepository(session)
        self._completion_repo = HabitCompletionRepository(session)
        self._session = session

    async def activate_habit(
        self, patient_id: uuid.UUID, template_id: str
    ) -> HabitTable:
        """Activate a new micro-habit from the template library."""
        active_count = await self._habit_repo.count_active(patient_id)
        if active_count >= MAX_ACTIVE_HABITS:
            raise ValueError(
                f"Maximum {MAX_ACTIVE_HABITS} habitudes actives. "
                "Desactivez-en une avant d'en ajouter."
            )

        template = HABIT_TEMPLATES.get(template_id)
        if template is None:
            raise ValueError(f"Modele d'habitude inconnu: {template_id}")

        row = HabitTable(
            patient_id=patient_id,
            template_id=template_id,
            name=template.name,
            dimension=template.dimension,
            started_at=datetime.now(tz=timezone.utc),
            is_active=True,
        )
        created = await self._habit_repo.create(row)
        await self._session.commit()
        return created

    async def complete_habit(
        self, habit_id: uuid.UUID, current_patient_id: uuid.UUID | None = None
    ) -> HabitCompletionTable:
        """Mark a habit as done for today."""
        habit = await self._habit_repo.get_by_id(habit_id)
        if habit is None:
            raise ValueError("Habitude introuvable")
        if current_patient_id is not None and habit.patient_id != current_patient_id:
            raise ValueError("Acces interdit a cette habitude")
        if not habit.is_active:
            raise ValueError("Cette habitude n'est plus active")

        today = date.today()
        existing = await self._completion_repo.get_by_habit_and_date(
            habit_id, today
        )
        if existing:
            raise ValueError("Habitude deja completee aujourd'hui")

        row = HabitCompletionTable(
            habit_id=habit_id,
            completed_date=today,
        )
        created = await self._completion_repo.create(row)
        await self._session.commit()
        return created

    async def get_active_habits_with_streaks(
        self, patient_id: uuid.UUID
    ) -> list[dict[str, object]]:
        """Get active habits with current streak and today's status."""
        habits = await self._habit_repo.get_active_habits(patient_id)
        result = []
        today = date.today()

        for habit in habits:
            completions = await self._completion_repo.get_completions_for_habit(
                habit.id, limit=60
            )
            streak = self._calculate_streak(completions, today)
            completed_today = any(c.completed_date == today for c in completions)

            result.append({
                "id": habit.id,
                "patient_id": habit.patient_id,
                "template_id": habit.template_id,
                "name": habit.name,
                "dimension": habit.dimension,
                "started_at": habit.started_at,
                "is_active": habit.is_active,
                "current_streak": streak,
                "completed_today": completed_today,
            })

        return result

    @staticmethod
    def _calculate_streak(
        completions: list[HabitCompletionTable], today: date
    ) -> int:
        """Calculate current consecutive day streak."""
        if not completions:
            return 0

        completion_dates = sorted(
            {c.completed_date for c in completions}, reverse=True
        )

        streak = 0
        expected = today
        for d in completion_dates:
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
