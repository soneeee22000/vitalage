import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.check_in_repository import CheckInRepository
from src.db.repositories.habit_repository import (
    HabitCompletionRepository,
    HabitRepository,
)
from src.db.repositories.meal_repository import MealRepository
from src.db.repositories.vitality_repository import VitalityScoreRepository
from src.db.tables import CheckInTable, HabitTable, MealTable, VitalityScoreTable

WEIGHT_NUTRITION = 0.30
WEIGHT_SLEEP = 0.25
WEIGHT_ACTIVITY = 0.25
WEIGHT_MOOD = 0.20

MOOD_SCORES: dict[str, int] = {
    "bien": 100,
    "content": 90,
    "calme": 80,
    "neutre": 60,
    "fatigue": 35,
    "stresse": 25,
    "irritable": 20,
}


class VitalityService:
    """Calculates and stores composite vitality scores."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._check_in_repo = CheckInRepository(session)
        self._meal_repo = MealRepository(session)
        self._habit_repo = HabitRepository(session)
        self._completion_repo = HabitCompletionRepository(session)
        self._score_repo = VitalityScoreRepository(session)

    async def recalculate(self, patient_id: uuid.UUID) -> VitalityScoreTable:
        """Recalculate vitality score from the last 7 days of data."""
        check_ins = await self._check_in_repo.get_recent(patient_id, limit=7)
        meals = await self._meal_repo.get_recent(patient_id, limit=7)
        habits = await self._habit_repo.get_active_habits(patient_id)

        nutrition = self._calc_nutrition(meals)
        sleep = self._calc_sleep(check_ins)
        activity = await self._calc_activity(habits, check_ins)
        mood = self._calc_mood(check_ins)

        overall = int(
            nutrition * WEIGHT_NUTRITION
            + sleep * WEIGHT_SLEEP
            + activity * WEIGHT_ACTIVITY
            + mood * WEIGHT_MOOD
        )
        overall = max(0, min(100, overall))

        row = VitalityScoreTable(
            patient_id=patient_id,
            nutrition=nutrition,
            sleep=sleep,
            activity=activity,
            mood=mood,
            overall=overall,
            calculated_at=datetime.now(tz=timezone.utc),
        )
        created = await self._score_repo.create(row)
        await self._session.commit()
        return created

    @staticmethod
    def _calc_nutrition(meals: list[MealTable]) -> int:
        """Nutrition score from meal quality and consistency."""
        if not meals:
            return 50

        quality_avg = sum(m.nutrition_score for m in meals) / len(meals)

        unique_days = len({m.date for m in meals})
        consistency = min(100, int((unique_days / 7) * 100))

        return max(0, min(100, int(quality_avg * 0.6 + consistency * 0.4)))

    @staticmethod
    def _calc_sleep(check_ins: list[CheckInTable]) -> int:
        """Sleep score from self-reported quality and consistency."""
        if not check_ins:
            return 50

        qualities = [ci.sleep_quality for ci in check_ins]
        quality_avg = sum(qualities) / len(qualities)
        quality_scaled = int((quality_avg / 5) * 100)

        if len(qualities) >= 3:
            mean = sum(qualities) / len(qualities)
            variance = sum((q - mean) ** 2 for q in qualities) / len(qualities)
            consistency = max(0, int(100 - variance * 20))
        else:
            consistency = 70

        return max(0, min(100, int(quality_scaled * 0.7 + consistency * 0.3)))

    async def _calc_activity(
        self,
        habits: list[HabitTable],
        check_ins: list[CheckInTable],
    ) -> int:
        """Activity score from habit completion rate and energy levels."""
        activity_habits = [h for h in habits if h.dimension == "activity"]

        if not activity_habits and not check_ins:
            return 50

        completion_score = 50
        if activity_habits:
            total_completions = 0
            total_possible = 0
            for habit in activity_habits:
                completions = await self._completion_repo.get_completions_for_habit(
                    habit.id, limit=7
                )
                total_completions += len(completions)
                total_possible += 7
            if total_possible > 0:
                completion_score = int(
                    (total_completions / total_possible) * 100
                )

        energy_score = 50
        if check_ins:
            energy_avg = sum(ci.energy_level for ci in check_ins) / len(
                check_ins
            )
            energy_score = int((energy_avg / 5) * 100)

        if activity_habits:
            return max(
                0, min(100, int(completion_score * 0.6 + energy_score * 0.4))
            )
        return max(0, min(100, energy_score))

    @staticmethod
    def _calc_mood(check_ins: list[CheckInTable]) -> int:
        """Mood score from reported mood, stability, and symptom frequency."""
        if not check_ins:
            return 50

        mood_values = [MOOD_SCORES.get(ci.mood, 50) for ci in check_ins]
        mood_avg = sum(mood_values) / len(mood_values)

        if len(mood_values) >= 3:
            mean = sum(mood_values) / len(mood_values)
            variance = sum((v - mean) ** 2 for v in mood_values) / len(
                mood_values
            )
            stability = max(0, int(100 - variance * 0.05))
        else:
            stability = 70

        symptom_count = sum(
            1 for ci in check_ins if ci.symptoms and ci.symptoms.strip()
        )
        symptom_penalty = min(30, symptom_count * 10)
        symptom_score = 100 - symptom_penalty

        return max(
            0,
            min(
                100,
                int(mood_avg * 0.6 + stability * 0.2 + symptom_score * 0.2),
            ),
        )
