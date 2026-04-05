import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class UserTable(Base):
    """Application user linked 1:1 with a FHIR Patient."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patients.id"), unique=True, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class PatientTable(Base):
    """Patient demographic record storing a FHIR Patient resource."""

    __tablename__ = "patients"

    fhir_resource: Mapped[dict] = mapped_column(JSONB, nullable=False)  # type: ignore[type-arg]
    identifier: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)


class CheckInTable(Base):
    """Daily vitality check-in (sleep, energy, mood, symptoms)."""

    __tablename__ = "check_ins"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False
    )
    sleep_quality: Mapped[int] = mapped_column(Integer, nullable=False)
    energy_level: Mapped[int] = mapped_column(Integer, nullable=False)
    mood: Mapped[str] = mapped_column(String(50), nullable=False)
    symptoms: Mapped[str | None] = mapped_column(Text, nullable=True)
    symptoms_structured: Mapped[dict | None] = mapped_column(JSONB, nullable=True)  # type: ignore[type-arg]
    date: Mapped[date] = mapped_column(Date, nullable=False)

    __table_args__ = (
        Index("ix_check_ins_patient_date", "patient_id", "date", unique=True),
    )


class MealTable(Base):
    """Meal photo analysis with AI-generated nutritional assessment."""

    __tablename__ = "meals"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False
    )
    photo_url: Mapped[str] = mapped_column(String(500), nullable=False)
    analysis: Mapped[dict] = mapped_column(JSONB, nullable=False)  # type: ignore[type-arg]
    nutrition_score: Mapped[int] = mapped_column(Integer, nullable=False)
    meal_type: Mapped[str] = mapped_column(String(20), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)

    __table_args__ = (
        Index("ix_meals_patient_date", "patient_id", "date"),
    )


class HabitTable(Base):
    """Active micro-habit tracked by a patient."""

    __tablename__ = "habits"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False
    )
    template_id: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    dimension: Mapped[str] = mapped_column(String(20), nullable=False)
    started_at: Mapped[datetime] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        Index("ix_habits_patient_active", "patient_id", "is_active"),
    )


class HabitCompletionTable(Base):
    """Daily completion record for a habit (one per habit per day)."""

    __tablename__ = "habit_completions"

    habit_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("habits.id"), nullable=False
    )
    completed_date: Mapped[date] = mapped_column(Date, nullable=False)

    __table_args__ = (
        Index(
            "ix_habit_completions_habit_date",
            "habit_id",
            "completed_date",
            unique=True,
        ),
    )


class VitalityScoreTable(Base):
    """Composite vitality score snapshot (recalculated on new data)."""

    __tablename__ = "vitality_scores"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False
    )
    nutrition: Mapped[int] = mapped_column(Integer, nullable=False)
    sleep: Mapped[int] = mapped_column(Integer, nullable=False)
    activity: Mapped[int] = mapped_column(Integer, nullable=False)
    mood: Mapped[int] = mapped_column(Integer, nullable=False)
    overall: Mapped[int] = mapped_column(Integer, nullable=False)
    calculated_at: Mapped[datetime] = mapped_column(nullable=False)

    __table_args__ = (
        Index("ix_vitality_scores_patient", "patient_id", "calculated_at"),
    )


class InsightTable(Base):
    """AI-generated personal health insight from correlation analysis."""

    __tablename__ = "insights"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False
    )
    insight_text: Mapped[str] = mapped_column(Text, nullable=False)
    insight_type: Mapped[str] = mapped_column(String(50), nullable=False)
    correlation_data: Mapped[dict] = mapped_column(JSONB, nullable=False)  # type: ignore[type-arg]
    generated_at: Mapped[datetime] = mapped_column(nullable=False)

    __table_args__ = (
        Index("ix_insights_patient", "patient_id"),
    )


class ConsentTable(Base):
    """FHIR Consent record for data processing authorization."""

    __tablename__ = "consents"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False
    )
    scope: Mapped[str] = mapped_column(String(100), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    fhir_resource: Mapped[dict] = mapped_column(JSONB, nullable=False)  # type: ignore[type-arg]

    __table_args__ = (
        Index("ix_consents_patient_scope", "patient_id", "scope"),
    )


class AuditEventTable(Base):
    """FHIR AuditEvent for tracking all AI agent calls."""

    __tablename__ = "audit_events"

    patient_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)
    agent_name: Mapped[str] = mapped_column(String(100), nullable=False)
    model_version: Mapped[str] = mapped_column(String(50), nullable=False)
    input_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    output_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    fhir_resource: Mapped[dict] = mapped_column(JSONB, nullable=False)  # type: ignore[type-arg]

    __table_args__ = (Index("ix_audit_events_patient_ref", "patient_ref"),)
