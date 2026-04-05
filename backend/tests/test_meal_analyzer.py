import base64

from src.agents.meal_analyzer import MealAnalyzer


def test_validate_base64_valid() -> None:
    """Valid base64 string passes validation."""
    encoded = base64.b64encode(b"fake image data").decode()
    assert MealAnalyzer.validate_base64(encoded) is True


def test_validate_base64_invalid() -> None:
    """Invalid base64 string fails validation."""
    assert MealAnalyzer.validate_base64("not-base64!!!") is False


def test_validate_base64_empty() -> None:
    """Empty string is valid base64 (decodes to empty bytes)."""
    assert MealAnalyzer.validate_base64("") is True
