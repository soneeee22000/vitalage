from datetime import date, datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error response."""

    detail: str
    code: str


class MoodEnum(str, Enum):
    """Mood options for daily check-in."""

    BIEN = "bien"
    CONTENT = "content"
    CALME = "calme"
    NEUTRE = "neutre"
    FATIGUE = "fatigue"
    STRESSE = "stresse"
    IRRITABLE = "irritable"


class MealTypeEnum(str, Enum):
    """Meal type classification."""

    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"


class RegisterRequest(BaseModel):
    """Request to register a new user account."""

    email: str = Field(min_length=5)
    password: str = Field(min_length=8)
    given_name: str = Field(min_length=1)
    family_name: str = Field(min_length=1)
    display_name: str = Field(min_length=1)


class LoginRequest(BaseModel):
    """Request to authenticate."""

    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    """JWT token pair response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    patient_id: str
    display_name: str


class RefreshRequest(BaseModel):
    """Request to refresh an access token."""

    refresh_token: str


class CheckInRequest(BaseModel):
    """Request to submit a daily check-in."""

    patient_id: UUID
    sleep_quality: int = Field(ge=1, le=5)
    energy_level: int = Field(ge=1, le=5)
    mood: MoodEnum
    symptoms: str | None = None


class CheckInResponse(BaseModel):
    """Response for a check-in."""

    id: UUID
    patient_id: UUID
    sleep_quality: int
    energy_level: int
    mood: str
    symptoms: str | None
    symptoms_structured: dict | None  # type: ignore[type-arg]
    date: date
    created_at: datetime


class CheckInStatusResponse(BaseModel):
    """Response for today's check-in status and streak."""

    completed_today: bool
    streak: int
    today_check_in: CheckInResponse | None = None


class MealAnalyzeRequest(BaseModel):
    """Request to analyze a meal photo."""

    patient_id: UUID
    image_base64: str = Field(description="Base64-encoded meal photo")
    meal_type: MealTypeEnum = MealTypeEnum.LUNCH


class MealResponse(BaseModel):
    """Response for a meal analysis."""

    id: UUID
    patient_id: UUID
    photo_url: str
    analysis: dict  # type: ignore[type-arg]
    nutrition_score: int
    meal_type: str
    date: date
    created_at: datetime


class ActivateHabitRequest(BaseModel):
    """Request to activate a new micro-habit."""

    patient_id: UUID
    template_id: str = Field(min_length=1)


class HabitResponse(BaseModel):
    """Response for a habit with streak info."""

    id: UUID
    patient_id: UUID
    template_id: str
    name: str
    dimension: str
    started_at: datetime
    is_active: bool
    current_streak: int
    completed_today: bool


class VitalityScoreResponse(BaseModel):
    """Response for the current vitality score."""

    patient_id: UUID
    nutrition: int
    sleep: int
    activity: int
    mood: int
    overall: int
    calculated_at: datetime
    change_from_last_week: int | None = None


class VitalityTrendPoint(BaseModel):
    """Single point in a vitality trend."""

    date: date
    overall: int
    nutrition: int
    sleep: int
    activity: int
    mood: int


class VitalityTrendResponse(BaseModel):
    """Response for vitality trends over time."""

    patient_id: UUID
    period: str
    data: list[VitalityTrendPoint]


class InsightResponse(BaseModel):
    """Response for an AI-generated insight."""

    id: UUID
    insight_text: str
    insight_type: str
    correlation_data: dict  # type: ignore[type-arg]
    generated_at: datetime
