from datetime import date
from unittest.mock import MagicMock

from src.services.vitality_service import VitalityService


def _mock_check_in(
    sleep: int = 4, energy: int = 3, mood: str = "bien", symptoms: str | None = None
) -> MagicMock:
    """Create a mock CheckInTable."""
    ci = MagicMock()
    ci.sleep_quality = sleep
    ci.energy_level = energy
    ci.mood = mood
    ci.symptoms = symptoms
    ci.date = date.today()
    return ci


def _mock_meal(score: int = 70, meal_date: date | None = None) -> MagicMock:
    """Create a mock MealTable."""
    m = MagicMock()
    m.nutrition_score = score
    m.date = meal_date or date.today()
    return m


def test_calc_sleep_high_quality() -> None:
    """Consistently good sleep produces a high score."""
    check_ins = [_mock_check_in(sleep=5) for _ in range(5)]
    score = VitalityService._calc_sleep(check_ins)
    assert score >= 85


def test_calc_sleep_low_quality() -> None:
    """Poor sleep produces a low score."""
    check_ins = [_mock_check_in(sleep=1) for _ in range(5)]
    score = VitalityService._calc_sleep(check_ins)
    assert score <= 50


def test_calc_sleep_empty() -> None:
    """No data returns baseline of 50."""
    assert VitalityService._calc_sleep([]) == 50


def test_calc_mood_positive() -> None:
    """Consistently positive mood produces high score."""
    check_ins = [_mock_check_in(mood="bien") for _ in range(5)]
    score = VitalityService._calc_mood(check_ins)
    assert score >= 80


def test_calc_mood_negative() -> None:
    """Stressed mood with symptoms produces low score."""
    check_ins = [
        _mock_check_in(mood="stresse", symptoms="mal de tete")
        for _ in range(5)
    ]
    score = VitalityService._calc_mood(check_ins)
    assert score <= 55


def test_calc_mood_empty() -> None:
    """No data returns baseline of 50."""
    assert VitalityService._calc_mood([]) == 50


def test_calc_nutrition_good_meals() -> None:
    """High-quality meals produce a high score."""
    meals = [_mock_meal(score=85) for _ in range(5)]
    score = VitalityService._calc_nutrition(meals)
    assert score >= 50


def test_calc_nutrition_no_meals() -> None:
    """No meals returns baseline of 50."""
    assert VitalityService._calc_nutrition([]) == 50


def test_calc_mood_stability_matters() -> None:
    """Unstable moods produce lower score than stable moods."""
    stable = [_mock_check_in(mood="calme") for _ in range(5)]
    unstable = [
        _mock_check_in(mood="bien"),
        _mock_check_in(mood="stresse"),
        _mock_check_in(mood="bien"),
        _mock_check_in(mood="stresse"),
        _mock_check_in(mood="bien"),
    ]
    stable_score = VitalityService._calc_mood(stable)
    unstable_score = VitalityService._calc_mood(unstable)
    assert stable_score > unstable_score


def test_scores_always_bounded() -> None:
    """All dimension scores stay within 0-100."""
    extremes_high = [_mock_check_in(sleep=5, energy=5, mood="bien") for _ in range(7)]
    extremes_low = [
        _mock_check_in(sleep=1, energy=1, mood="irritable", symptoms="douleur")
        for _ in range(7)
    ]

    for calc in [VitalityService._calc_sleep, VitalityService._calc_mood]:
        high = calc(extremes_high)
        low = calc(extremes_low)
        assert 0 <= high <= 100
        assert 0 <= low <= 100
