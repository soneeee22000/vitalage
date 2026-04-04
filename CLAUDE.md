# VitalAge — Project CLAUDE.md

## Project Overview

VitalAge is a daily vitality companion for smart aging — 60-second check-ins that build into a personal health equation. Built for the Nestle Vital VivaTech 2026 challenge ("Smart Aging"). Focus: preventive health through sustainable micro-habits. French market first.

## Tech Stack

- **Backend:** Python 3.12, FastAPI, SQLAlchemy async, Alembic, Mistral AI SDK
- **Frontend:** React 19, TypeScript (strict), Tailwind CSS, shadcn/ui, PWA (vite-plugin-pwa)
- **Database:** PostgreSQL 16 (FHIR R5 JSONB via asyncpg)
- **FHIR:** fhir.resources 8.x (R5) for data model validation
- **AI Models:** Mistral Small (check-in analysis, meal interpretation, insight generation, habit recommendation), Mistral OCR (meal photo analysis), Voxtral (voice check-ins)
- **Auth:** JWT (python-jose) + bcrypt (passlib)
- **Deployment:** Docker, Google Cloud Run
- **Testing:** pytest (backend), vitest (frontend), Playwright (E2E)

## Architecture Rules

- Clean Architecture: agents/ (AI logic) -> services/ (business logic) -> api/ (routes)
- All data stored as FHIR R5 resources where applicable
- All Mistral API calls go through agents/ via `mistral_utils.safe_chat_complete`
- Every AI agent call is audit-logged as a FHIR AuditEvent
- All AI-powered endpoints require active FHIR Consent
- JWT auth with user data isolation
- Database access goes through repositories (db/repositories/)
- Frontend uses `useAsyncData` hook for all data fetching
- Frontend is mobile-first PWA with accessibility focus (45-70 demographic)
- All API responses include structured error handling; French contextual messages

## Design System

- Warm, inviting, accessible (not clinical, not sporty)
- Soft earth tones with vitality green accents
- Accessibility-first: 44px touch targets, 18px minimum body font (larger for older demographic)
- Typography: Lora (headings), Inter (body) — larger sizes than typical
- Gamification: streak flames, progress rings, celebration animations
- No emojis as icons — use Lucide icons
- No gradients on buttons
- Color-coded vitality dimensions (nutrition=green, sleep=blue, activity=orange, mood=purple)

## Key Screens

1. **Check-in** — morning 60-second ritual (sleep, energy, mood, optional symptoms)
2. **Meals** — photograph meals, AI nutritional analysis with positive framing
3. **Vitality** — composite score (0-100) with 4-dimension breakdown and trends
4. **Habits** — 3 active micro-habits with Duolingo-style streaks
5. **Insights** — AI-generated personal correlations ("when you do X, you feel Y")

## API Design

### Public

- GET /health
- POST /auth/register
- POST /auth/login
- POST /auth/refresh

### Protected

- POST /api/v1/check-ins — submit daily check-in
- GET /api/v1/check-ins/patients/{id} — check-in history
- POST /api/v1/meals/analyze — meal photo upload -> nutritional analysis
- GET /api/v1/meals/patients/{id} — meal history
- GET /api/v1/vitality/patients/{id} — current vitality score + history
- GET /api/v1/vitality/patients/{id}/trends — weekly/monthly trends
- POST /api/v1/habits/activate — start a new habit
- POST /api/v1/habits/{id}/complete — mark habit done today
- GET /api/v1/habits/patients/{id} — active habits with streaks
- GET /api/v1/insights/patients/{id} — personalized AI insights
- POST /api/v1/consents — record consent
- PUT /api/v1/consents/{id}/revoke — revoke consent
- GET /api/v1/audit-events — audit log

## Vitality Score Algorithm

4 dimensions, each 0-100, weighted composite:

- Nutrition (30%): meal quality, nutrient diversity, consistency
- Sleep (25%): self-reported quality, consistency
- Activity (25%): self-reported activity, habit completion rate
- Mood (20%): mood reports, mood stability, symptom frequency

Overall Vitality = weighted sum, recalculated on each new data point.
Trends computed on 7-day rolling windows.

## Quality Gates

- Same as Entre Deux: ruff + mypy strict + pytest-cov 80% + TypeScript strict
- No TODO comments
- Type hints on all Python functions
- Max 30 lines per function
- All 3 test suites pass before submission
- Accessibility audit: all interactive elements have aria labels, contrast ratio 4.5:1+

## Reuse from Entre Deux

This project reuses significant code from ~/entre-deux:

- mistral_utils.py (safe_chat_complete, safe_json_parse, AgentError)
- Journal agent patterns (adapted for check-in analysis)
- Voice transcription agent (Voxtral for voice check-ins)
- Auth middleware (JWT + user isolation)
- Consent middleware (FHIR consent enforcement)
- Audit logging service
- React project scaffold (Tailwind + shadcn + PWA config)
- useAsyncData hook
- Error boundaries
- Docker + Cloud Run deployment config
