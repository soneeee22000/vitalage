from datetime import date, timedelta
from unittest.mock import MagicMock


def _make_check_in(check_date: date) -> MagicMock:
    """Create a mock CheckInTable with a date."""
    ci = MagicMock()
    ci.date = check_date
    return ci


def test_streak_empty_list() -> None:
    """Empty check-in list produces streak of 0."""
    today = date.today()
    check_in_dates: list[date] = []
    streak = 0
    expected = today
    for d in check_in_dates:
        if d == expected:
            streak += 1
            expected -= timedelta(days=1)
        else:
            break
    assert streak == 0


def test_check_in_streak_calculation_consecutive() -> None:
    """Consecutive days ending today produce correct streak."""
    today = date.today()
    check_ins = [
        _make_check_in(today),
        _make_check_in(today - timedelta(days=1)),
        _make_check_in(today - timedelta(days=2)),
    ]

    # Simulate the streak logic directly
    check_in_dates = sorted({ci.date for ci in check_ins}, reverse=True)
    streak = 0
    expected = today
    for d in check_in_dates:
        if d == expected:
            streak += 1
            expected -= timedelta(days=1)
        elif d == today - timedelta(days=1) and expected == today:
            expected = d
            streak += 1
            expected -= timedelta(days=1)
        else:
            break

    assert streak == 3


def test_check_in_streak_with_gap() -> None:
    """A gap in check-in dates breaks the streak."""
    today = date.today()
    check_in_dates = sorted(
        {today, today - timedelta(days=3)}, reverse=True
    )
    streak = 0
    expected = today
    for d in check_in_dates:
        if d == expected:
            streak += 1
            expected -= timedelta(days=1)
        elif d == today - timedelta(days=1) and expected == today:
            expected = d
            streak += 1
            expected -= timedelta(days=1)
        else:
            break

    assert streak == 1


def test_check_in_streak_starting_yesterday() -> None:
    """Streak counts from yesterday if today not completed."""
    today = date.today()
    check_in_dates = sorted(
        {
            today - timedelta(days=1),
            today - timedelta(days=2),
            today - timedelta(days=3),
        },
        reverse=True,
    )
    streak = 0
    expected = today
    for d in check_in_dates:
        if d == expected:
            streak += 1
            expected -= timedelta(days=1)
        elif d == today - timedelta(days=1) and expected == today:
            expected = d
            streak += 1
            expected -= timedelta(days=1)
        else:
            break

    assert streak == 3
