from datetime import date
from unittest.mock import MagicMock

from src.services.insight_service import InsightService


def _mock_check_in(
    check_date: date,
    sleep: int = 4,
    energy: int = 3,
    mood: str = "bien",
    symptoms: str | None = None,
) -> MagicMock:
    """Create a mock CheckInTable."""
    ci = MagicMock()
    ci.date = check_date
    ci.sleep_quality = sleep
    ci.energy_level = energy
    ci.mood = mood
    ci.symptoms = symptoms
    return ci


def test_build_data_summary_formats_correctly() -> None:
    """Data summary includes all check-in fields."""
    check_ins = [
        _mock_check_in(date(2026, 4, 1), sleep=5, energy=4, mood="bien"),
        _mock_check_in(
            date(2026, 4, 2), sleep=3, energy=2,
            mood="fatigue", symptoms="Mal de tete",
        ),
    ]
    summary = InsightService._build_data_summary(check_ins)

    assert "2026-04-01" in summary
    assert "sommeil=5/5" in summary
    assert "energie=4/5" in summary
    assert "humeur=bien" in summary
    assert "2026-04-02" in summary
    assert "Mal de tete" in summary


def test_build_data_summary_empty() -> None:
    """Empty check-ins produce empty summary."""
    summary = InsightService._build_data_summary([])
    assert summary == ""


def test_build_data_summary_no_symptoms() -> None:
    """Check-in without symptoms omits symptom text."""
    check_ins = [_mock_check_in(date(2026, 4, 1))]
    summary = InsightService._build_data_summary(check_ins)
    assert "symptomes" not in summary
