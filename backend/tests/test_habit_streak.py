from datetime import date, timedelta
from unittest.mock import MagicMock

from src.services.habit_service import HabitService


def _make_completion(completed_date: date) -> MagicMock:
    """Create a mock HabitCompletionTable with a date."""
    c = MagicMock()
    c.completed_date = completed_date
    return c


def test_streak_no_completions() -> None:
    """Empty completions returns streak of 0."""
    assert HabitService._calculate_streak([], date.today()) == 0


def test_streak_consecutive_days() -> None:
    """Consecutive completions ending today produce correct streak."""
    today = date.today()
    completions = [
        _make_completion(today),
        _make_completion(today - timedelta(days=1)),
        _make_completion(today - timedelta(days=2)),
    ]
    assert HabitService._calculate_streak(completions, today) == 3


def test_streak_gap_breaks_streak() -> None:
    """A gap in completions breaks the streak."""
    today = date.today()
    completions = [
        _make_completion(today),
        _make_completion(today - timedelta(days=2)),
    ]
    assert HabitService._calculate_streak(completions, today) == 1


def test_streak_not_completed_today() -> None:
    """If today is not completed, streak counts from yesterday."""
    today = date.today()
    completions = [
        _make_completion(today - timedelta(days=1)),
        _make_completion(today - timedelta(days=2)),
    ]
    streak = HabitService._calculate_streak(completions, today)
    assert streak == 2
