"""Seed demo account: Marie, 58, retired teacher from Lyon.

30 days of check-ins showing vitality progression from 52 to 76.
3 active habits with realistic streaks.
5 pre-generated insights.
15 meal analyses.

Usage: python -m scripts.seed_demo
"""

import asyncio
import os
import random
import uuid
from datetime import date, datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.engine import async_session_factory
from src.db.tables import (
    CheckInTable,
    ConsentTable,
    HabitCompletionTable,
    HabitTable,
    InsightTable,
    MealTable,
    PatientTable,
    UserTable,
    VitalityScoreTable,
)
from src.models.fhir_helpers import create_consent, create_patient
from src.services.auth_service import pwd_context

MARIE_EMAIL = "marie.dupont@demo.vitalage.health"
MARIE_CRED = os.environ.get("DEMO_CRED", "vitalage2026")

MOODS = ["bien", "calme", "neutre", "fatigue", "stresse"]
MOOD_WEIGHTS_EARLY = [0.15, 0.15, 0.30, 0.25, 0.15]
MOOD_WEIGHTS_LATE = [0.30, 0.30, 0.25, 0.10, 0.05]

DEMO_MEALS = [
    {
        "summary": "Salade nicoise avec oeuf et olives",
        "foods": ["salade", "oeuf", "tomate", "olives", "thon"],
        "highlights": ["Riche en proteines", "Bonne source d'omega-3"],
        "tip": "Ajoutez un peu de pain complet pour les fibres",
        "score": 78,
    },
    {
        "summary": "Soupe de legumes maison avec pain",
        "foods": ["carotte", "poireau", "pomme de terre", "pain"],
        "highlights": ["Riche en fibres", "Bonne hydratation"],
        "tip": "Parfait pour le soir, leger et nutritif",
        "score": 82,
    },
    {
        "summary": "Omelette aux champignons et salade verte",
        "foods": ["oeuf", "champignon", "salade", "fromage"],
        "highlights": ["Proteines de qualite", "Vitamines B"],
        "tip": "Les champignons sont excellents pour l'immunite",
        "score": 75,
    },
    {
        "summary": "Tartine avocat et saumon fume",
        "foods": ["pain complet", "avocat", "saumon fume", "citron"],
        "highlights": ["Omega-3", "Bonnes graisses", "Fibres"],
        "tip": "Un excellent choix pour le coeur",
        "score": 88,
    },
    {
        "summary": "Ratatouille avec riz complet",
        "foods": ["aubergine", "courgette", "tomate", "poivron", "riz"],
        "highlights": ["Riche en legumes", "Antioxydants"],
        "tip": "Variez les couleurs pour plus de nutriments",
        "score": 85,
    },
    {
        "summary": "Quiche lorraine et salade",
        "foods": ["pate", "lardons", "oeuf", "creme", "salade"],
        "highlights": ["Proteines", "Calcium"],
        "tip": "La salade equilibre bien ce plat riche",
        "score": 62,
    },
    {
        "summary": "Yaourt grec avec fruits et miel",
        "foods": ["yaourt", "fraise", "myrtille", "miel", "granola"],
        "highlights": ["Probiotiques", "Vitamines C", "Calcium"],
        "tip": "Parfait en collation ou petit-dejeuner",
        "score": 80,
    },
]

DEMO_INSIGHTS = [
    {
        "text": "Quand vous dormez plus de 4/5, votre energie "
        "le lendemain est 40% plus elevee",
        "type": "correlation",
        "data": {
            "dimension_a": "sleep",
            "dimension_b": "energy",
            "direction": "positive",
            "strength": "strong",
        },
    },
    {
        "text": "Les jours ou vous marchez apres le dejeuner, "
        "votre humeur est systematiquement meilleure",
        "type": "correlation",
        "data": {
            "dimension_a": "activity",
            "dimension_b": "mood",
            "direction": "positive",
            "strength": "strong",
        },
    },
    {
        "text": "Vos repas riches en legumes sont suivis de "
        "meilleures nuits de sommeil",
        "type": "correlation",
        "data": {
            "dimension_a": "nutrition",
            "dimension_b": "sleep",
            "direction": "positive",
            "strength": "moderate",
        },
    },
    {
        "text": "Votre humeur est plus stable en milieu de semaine "
        "qu'en fin de semaine",
        "type": "trend",
        "data": {
            "dimension_a": "mood",
            "dimension_b": "mood",
            "direction": "positive",
            "strength": "moderate",
        },
    },
    {
        "text": "Les jours avec symptomes, votre energie du "
        "lendemain baisse de 25%",
        "type": "correlation",
        "data": {
            "dimension_a": "mood",
            "dimension_b": "energy",
            "direction": "negative",
            "strength": "moderate",
        },
    },
]


async def seed_demo() -> None:
    """Create Marie's demo account with 30 days of data."""
    async with async_session_factory() as session:
        existing = await _check_existing(session)
        if existing:
            print(f"Demo account already exists: {MARIE_EMAIL}")
            return

        patient_id = await _create_user(session)
        await _create_check_ins(session, patient_id)
        await _create_meals(session, patient_id)
        habit_ids = await _create_habits(session, patient_id)
        await _create_habit_completions(session, habit_ids)
        await _create_vitality_scores(session, patient_id)
        await _create_insights(session, patient_id)
        await session.commit()

        print(f"Demo account seeded: {MARIE_EMAIL} / {MARIE_CRED}")
        print(f"Patient ID: {patient_id}")


async def _check_existing(session: AsyncSession) -> bool:
    """Check if demo account already exists."""
    from sqlalchemy import select

    stmt = select(UserTable).where(UserTable.email == MARIE_EMAIL)
    result = await session.execute(stmt)
    return result.scalar_one_or_none() is not None


async def _create_user(session: AsyncSession) -> uuid.UUID:
    """Create Marie's user + patient + consent."""
    identifier = "VA-DEMO0001"
    fhir_patient = create_patient("Marie", "Dupont", identifier)
    patient = PatientTable(
        identifier=identifier,
        fhir_resource=fhir_patient.model_dump(mode="json"),
    )
    session.add(patient)
    await session.flush()
    await session.refresh(patient)
    patient.fhir_resource["id"] = str(patient.id)

    user = UserTable(
        email=MARIE_EMAIL,
        password_hash=pwd_context.hash(MARIE_CRED),
        display_name="Marie",
        patient_id=patient.id,
        is_active=True,
    )
    session.add(user)

    fhir_consent = create_consent(
        f"Patient/{patient.id}", "ai-processing"
    )
    consent = ConsentTable(
        patient_id=patient.id,
        scope="ai-processing",
        active=True,
        fhir_resource=fhir_consent.model_dump(mode="json"),
    )
    session.add(consent)
    await session.flush()

    print(f"Created user Marie (patient_id={patient.id})")
    return patient.id


async def _create_check_ins(
    session: AsyncSession, patient_id: uuid.UUID
) -> None:
    """Create 30 days of check-ins with improving trajectory."""
    today = date.today()

    for day_offset in range(30, 0, -1):
        check_date = today - timedelta(days=day_offset)
        progress = 1 - (day_offset / 30)

        sleep = _weighted_choice(
            [1, 2, 3, 4, 5],
            _shift_weights([0.05, 0.15, 0.30, 0.30, 0.20], progress),
        )
        energy = _weighted_choice(
            [1, 2, 3, 4, 5],
            _shift_weights([0.10, 0.20, 0.30, 0.25, 0.15], progress),
        )
        mood_weights = [
            a + (b - a) * progress
            for a, b in zip(MOOD_WEIGHTS_EARLY, MOOD_WEIGHTS_LATE, strict=False)
        ]
        mood = random.choices(MOODS, weights=mood_weights, k=1)[0]

        symptoms = None
        if random.random() < (0.3 - progress * 0.2):
            symptoms = random.choice([
                "Legere fatigue",
                "Douleur au dos",
                "Mal de tete",
            ])

        skip_day = random.random() < 0.08
        if skip_day:
            continue

        ci = CheckInTable(
            patient_id=patient_id,
            sleep_quality=sleep,
            energy_level=energy,
            mood=mood,
            symptoms=symptoms,
            symptoms_structured=None,
            date=check_date,
            created_at=datetime(
                check_date.year,
                check_date.month,
                check_date.day,
                7,
                30,
                tzinfo=timezone.utc,
            ),
        )
        session.add(ci)

    await session.flush()
    print("Created ~28 check-ins over 30 days")


async def _create_meals(
    session: AsyncSession, patient_id: uuid.UUID
) -> None:
    """Create 15 meal analyses spread across 30 days."""
    today = date.today()
    meal_count = 0

    for day_offset in range(30, 0, -2):
        if meal_count >= 15:
            break
        meal_date = today - timedelta(days=day_offset)
        meal_data = random.choice(DEMO_MEALS)
        meal_type = random.choice(["lunch", "dinner"])

        meal = MealTable(
            patient_id=patient_id,
            photo_url=f"demo://{patient_id}/{meal_date}/{meal_type}",
            analysis={
                "foods_identified": meal_data["foods"],
                "nutritional_highlights": meal_data["highlights"],
                "quality_score": meal_data["score"],
                "micro_tip": meal_data["tip"],
                "summary": meal_data["summary"],
            },
            nutrition_score=meal_data["score"],
            meal_type=meal_type,
            date=meal_date,
            created_at=datetime(
                meal_date.year,
                meal_date.month,
                meal_date.day,
                12,
                30,
                tzinfo=timezone.utc,
            ),
        )
        session.add(meal)
        meal_count += 1

    await session.flush()
    print(f"Created {meal_count} meal analyses")


async def _create_habits(
    session: AsyncSession, patient_id: uuid.UUID
) -> list[uuid.UUID]:
    """Create 3 active habits started at different times."""
    habits_config = [
        ("walk-after-lunch", "Marcher 10 min apres le dejeuner", "activity", 20),
        ("fruit-before-noon", "1 fruit avant midi", "nutrition", 14),
        ("sleep-before-23h", "Dormir avant 23h", "sleep", 10),
    ]
    habit_ids = []
    today = date.today()

    for template_id, name, dimension, days_ago in habits_config:
        habit = HabitTable(
            patient_id=patient_id,
            template_id=template_id,
            name=name,
            dimension=dimension,
            started_at=datetime(
                (today - timedelta(days=days_ago)).year,
                (today - timedelta(days=days_ago)).month,
                (today - timedelta(days=days_ago)).day,
                8,
                0,
                tzinfo=timezone.utc,
            ),
            is_active=True,
        )
        session.add(habit)
        await session.flush()
        await session.refresh(habit)
        habit_ids.append(habit.id)

    print("Created 3 active habits")
    return habit_ids


async def _create_habit_completions(
    session: AsyncSession, habit_ids: list[uuid.UUID]
) -> None:
    """Create realistic habit completions with some missed days."""
    today = date.today()
    streaks = [12, 5, 8]

    for habit_id, streak_length in zip(habit_ids, streaks, strict=False):
        for day_offset in range(streak_length):
            comp_date = today - timedelta(days=day_offset)
            comp = HabitCompletionTable(
                habit_id=habit_id,
                completed_date=comp_date,
            )
            session.add(comp)

    await session.flush()
    print("Created habit completions (streaks: 12, 5, 8)")


async def _create_vitality_scores(
    session: AsyncSession, patient_id: uuid.UUID
) -> None:
    """Create vitality scores showing 52→76 progression."""
    today = date.today()
    base_scores = {
        "nutrition": 45,
        "sleep": 55,
        "activity": 40,
        "mood": 50,
    }

    for day_offset in range(28, 0, -1):
        score_date = today - timedelta(days=day_offset)
        progress = 1 - (day_offset / 28)

        noise = random.randint(-3, 3)
        nutrition = min(100, base_scores["nutrition"] + int(progress * 30) + noise)
        sleep = min(100, base_scores["sleep"] + int(progress * 25) + noise)
        activity = min(100, base_scores["activity"] + int(progress * 28) + noise)
        mood = min(100, base_scores["mood"] + int(progress * 22) + noise)

        overall = int(
            nutrition * 0.30
            + sleep * 0.25
            + activity * 0.25
            + mood * 0.20
        )

        score = VitalityScoreTable(
            patient_id=patient_id,
            nutrition=nutrition,
            sleep=sleep,
            activity=activity,
            mood=mood,
            overall=overall,
            calculated_at=datetime(
                score_date.year,
                score_date.month,
                score_date.day,
                8,
                0,
                tzinfo=timezone.utc,
            ),
        )
        session.add(score)

    await session.flush()
    print("Created 28 vitality score snapshots (52→76)")


async def _create_insights(
    session: AsyncSession, patient_id: uuid.UUID
) -> None:
    """Create 5 pre-generated insights."""
    now = datetime.now(tz=timezone.utc)

    for insight_data in DEMO_INSIGHTS:
        insight = InsightTable(
            patient_id=patient_id,
            insight_text=insight_data["text"],
            insight_type=insight_data["type"],
            correlation_data=insight_data["data"],
            generated_at=now,
        )
        session.add(insight)

    await session.flush()
    print("Created 5 AI insights")


def _weighted_choice(values: list[int], weights: list[float]) -> int:
    """Random choice with weights."""
    return random.choices(values, weights=weights, k=1)[0]


def _shift_weights(
    base: list[float], progress: float
) -> list[float]:
    """Shift weights toward higher values as progress increases."""
    shifted = []
    n = len(base)
    for i, w in enumerate(base):
        boost = progress * 0.1 * (i / (n - 1))
        penalty = progress * 0.05 * (1 - i / (n - 1))
        shifted.append(max(0.01, w + boost - penalty))
    total = sum(shifted)
    return [w / total for w in shifted]


if __name__ == "__main__":
    asyncio.run(seed_demo())
