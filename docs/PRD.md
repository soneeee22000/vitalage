# PRD: VitalAge

> **Status:** Draft
> **Author:** Pyae Sone (Seon)
> **Date:** 2026-04-05
> **Last Updated:** 2026-04-05

---

## 1. Problem Statement

### What problem are we solving?

Health apps are abandoned in 7 days because they have no feedback loop. Users log food, sleep, mood — nothing comes back. No insight, no pattern, no reason to return. Meanwhile, 14M+ French adults over 60 have zero accessible digital health companions. Existing solutions require expensive hardware (Whoop $30/mo, Oura $300+) or punish with calorie counting (MyFitnessPal, 80% dropout by month 2). Nobody serves the 45-70 "smart aging" demographic with positive, science-backed daily health companionship.

### Who has this problem?

French adults aged 45-70 who want to age well. Health-conscious but not fitness enthusiasts. May be managing early chronic conditions (pre-diabetes, cholesterol, joint pain). Value quality of life and food culture over calorie restriction. Own a smartphone but don't use fitness trackers.

### Why now?

- France's "silver economy" is a national strategic priority
- 60+ population growing from 14M to 20M by 2030
- Multimodal AI (Mistral vision, LLM reasoning) now enables phone-only health analysis without wearables
- Nestle Vital VivaTech 2026 challenge specifically targets this exact problem space
- Deadline: April 27, 2026

---

## 2. Success Criteria

### Primary Metric

A judge at VivaTech can complete a full check-in in under 60 seconds and immediately see their Vitality Score change — demonstrating the feedback loop that makes VitalAge different.

### Secondary Metrics

- [ ] Working live demo on production URL with seeded 30-day data
- [ ] Meal photo analysis returns sensible nutritional assessment for common French meals
- [ ] 80%+ test coverage on critical backend paths
- [ ] Full demo walkthrough completes in under 3 minutes
- [ ] All UI in French, accessible (18px+ font, 44px+ touch targets, 4.5:1 contrast)

### What does "done" look like?

A deployed PWA where a user can: register, complete a 60-second morning check-in (sleep/energy/mood/symptoms), photograph a meal and receive AI nutritional feedback, view their Vitality Score (0-100) with 4-dimension breakdown and trends, maintain 3 micro-habit streaks, and read AI-generated personal health insights. Demo account "Marie, 58, Lyon" shows a compelling 30-day journey from Vitality 52 to 76.

---

## 3. User Stories & Acceptance Criteria

### Story 1: Morning Check-in (T1 — Must Ship)

**As a** health-conscious adult 50+, **I want to** complete a 60-second morning check-in about my sleep, energy, mood, and symptoms, **so that** I build a daily health data record and see my vitality respond.

**Acceptance Criteria:**

- [ ] Given I'm logged in, when I open the app, then I see the check-in screen with my name and today's date
- [ ] Given I'm on the check-in screen, when I tap sleep quality (1-5), energy (1-5), mood (selection), and optionally enter symptoms, then I can submit in under 60 seconds
- [ ] Given I submit a check-in, when the server processes it, then my Vitality Score recalculates and I see a celebration animation
- [ ] Given I already submitted today, when I open the check-in screen, then I see "Bilan complété" with my streak count
- [ ] Error state: when the server is unreachable, then I see a clear error message with a retry button

### Story 2: Vitality Score Dashboard (T1 — Must Ship)

**As a** user with 3+ days of check-ins, **I want to** see my Vitality Score (0-100) with a 4-dimension breakdown, **so that** I understand which aspects of my health are strong and which need attention.

**Acceptance Criteria:**

- [ ] Given I have check-in data, when I view the Vitality screen, then I see a large circular score (0-100) with animated fill
- [ ] Given I have a score, when I view the dashboard, then I see 4 dimension bars: Nutrition (green), Sommeil (blue), Activité (orange), Humeur (purple)
- [ ] Given I have 7+ days of data, when I view the dashboard, then I see a weekly trend sparkline and a change indicator ("+3 depuis la semaine dernière")
- [ ] Given I'm a new user with <3 days of data, when I view the dashboard, then I see a "keep checking in" prompt instead of an incomplete score
- [ ] Error state: when score calculation fails, then I see the last known score with a "mise à jour en cours" indicator

### Story 3: Micro-Habits with Streaks (T1 — Must Ship)

**As a** user who wants to improve a weak vitality dimension, **I want to** maintain 3 active micro-habits with streak tracking, **so that** small daily actions compound into measurable vitality improvement.

**Acceptance Criteria:**

- [ ] Given I'm a new user, when I first visit habits, then the system recommends 3 habits targeting my weakest vitality dimension
- [ ] Given I have active habits, when I tap "complete" on a habit, then my streak increments and I see a satisfying animation
- [ ] Given I have a 7+ day streak, when I complete a habit, then the streak flame icon intensifies
- [ ] Given I miss a day, when I return, then my streak resets to 0 with encouragement ("Pas grave, on recommence!")
- [ ] Given all 3 habits have 7+ day streaks, when I view habits, then I see a suggestion to level up or swap one habit
- [ ] Error state: when habit completion fails to save, then I see a retry option and the UI does not show a false completion

### Story 4: Meal Photo Analysis (T2 — Should Ship)

**As a** user eating a meal, **I want to** photograph my food and receive instant AI nutritional feedback, **so that** I understand my nutritional intake without calorie counting.

**Acceptance Criteria:**

- [ ] Given I'm on the meals screen, when I tap the camera button, then my phone camera opens with a food framing guide
- [ ] Given I take a meal photo, when the AI processes it, then I see: identified foods, nutritional highlights (positive framing), quality score, and one actionable micro-tip
- [ ] Given the AI analyzes a meal, when results appear, then the language is positive ("Riche en fibres et protéines") never punitive ("Too many calories")
- [ ] Given I have meal history, when I view the meals screen, then I see a gallery of past meals with their nutrition scores
- [ ] Error state: when the AI cannot identify the food, then I see "Nous n'avons pas pu analyser cette photo. Essayez avec un meilleur éclairage."

### Story 5: Personal AI Insights (T3 — Seeded Demo)

**As a** user with 2+ weeks of data, **I want to** see AI-generated correlations between my behaviors and outcomes, **so that** I discover my personal health equation.

**Acceptance Criteria:**

- [ ] Given I have <14 days of data, when I view insights, then I see a locked state: "Continuez vos bilans pour débloquer vos insights personnels"
- [ ] Given I have 14+ days of data, when I view insights, then I see card-based correlations: "Quand vous dormez plus de 7h, votre énergie le lendemain est 40% plus élevée"
- [ ] Given an insight is displayed, when I read it, then it includes a simple visual (bar chart or comparison) showing the correlation
- [ ] Given the demo account (Marie), when I view her insights, then I see 5 pre-generated insights with real correlation data from her 30-day journey

### Story 6: Authentication (Foundation)

**As a** new user, **I want to** register and log in securely, **so that** my health data is private and isolated from other users.

**Acceptance Criteria:**

- [ ] Given I'm a new user, when I register with email/password, then my account is created and I'm logged in with JWT tokens
- [ ] Given I'm returning, when I log in with valid credentials, then I receive access + refresh tokens
- [ ] Given my access token expires, when I make an API call, then the client silently refreshes the token
- [ ] Given I'm logged in, when I access API endpoints, then I only see my own data (patient isolation)
- [ ] Error state: when credentials are invalid, then I see "Email ou mot de passe incorrect"

---

## 4. Technical Architecture

### Stack Decision

| Layer    | Choice                                                                      | Why                                                                        |
| -------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Frontend | React 19 + TypeScript strict + Tailwind + shadcn/ui + PWA (vite-plugin-pwa) | Proven stack from Entre Deux, PWA for installability without app stores    |
| Backend  | Python 3.12 + FastAPI + SQLAlchemy async + Alembic                          | Reuse 90% from Entre Deux, async for AI agent calls                        |
| Database | PostgreSQL 16 (asyncpg)                                                     | JSONB for flexible health data, proven from Entre Deux                     |
| AI       | Mistral Small (analysis/insights) + Mistral OCR/Vision (meal photos)        | European AI (EU data residency), competitive pricing, proven in Entre Deux |
| Auth     | JWT (python-jose) + bcrypt (passlib)                                        | Reuse 100% from Entre Deux                                                 |
| Hosting  | Docker + Google Cloud Run                                                   | Reuse 100% deployment pipeline                                             |
| CI/CD    | GitHub Actions (ruff + mypy + pytest + vitest + build)                      | Reuse from Entre Deux                                                      |

### Architecture Diagram

```
┌───────────────────────────────────────────────┐
│              FRONTEND (PWA)                    │
│  React 19 + TypeScript + Tailwind + shadcn    │
│                                                │
│  Pages: Bilan | Repas | Vitalité |            │
│         Habitudes | Insights                   │
│  Auth: JWT (localStorage)                      │
│  Data: useAsyncData hook                       │
│  Lang: French only                             │
│  A11y: 18px+ body, 44px+ targets              │
└──────────────────┬────────────────────────────┘
                   │ HTTPS (JSON)
┌──────────────────▼────────────────────────────┐
│              BACKEND (FastAPI)                  │
│                                                │
│  api/v1/                                       │
│    auth.py         POST register/login/refresh │
│    check_ins.py    POST submit, GET history    │
│    meals.py        POST analyze, GET history   │
│    vitality.py     GET score, GET trends       │
│    habits.py       POST activate/complete, GET │
│    insights.py     GET personal insights       │
│                                                │
│  agents/                                       │
│    mistral_utils.py    (reuse 100%)            │
│    check_in_analyzer.py                        │
│    meal_analyzer.py                            │
│    insight_engine.py                           │
│    habit_recommender.py                        │
│                                                │
│  services/                                     │
│    auth_service.py     (reuse 100%)            │
│    check_in_service.py                         │
│    meal_service.py                             │
│    vitality_service.py                         │
│    habit_service.py                            │
│    insight_service.py                          │
│    audit_service.py    (reuse 100%)            │
│                                                │
│  middleware/                                   │
│    auth.py             (reuse 100%)            │
│    consent.py          (reuse 100%)            │
│    rate_limit.py       (reuse 100%)            │
│                                                │
│  db/                                           │
│    base.py             (reuse 100%)            │
│    engine.py           (reuse 100%)            │
│    tables.py           (extend with new tables)│
│    repositories/       (extend with new repos) │
└──────────────────┬────────────────────────────┘
                   │
┌──────────────────▼────────────────────────────┐
│            PostgreSQL 16                       │
│  users, patients, consents, audit_events       │
│  + check_ins, meals, habits,                   │
│    habit_completions, vitality_scores, insights │
└───────────────────────────────────────────────┘
```

### API Design

| Method | Endpoint                              | Purpose                    | Auth |
| ------ | ------------------------------------- | -------------------------- | ---- |
| POST   | /auth/register                        | Create account             | No   |
| POST   | /auth/login                           | Get JWT tokens             | No   |
| POST   | /auth/refresh                         | Refresh access token       | No   |
| GET    | /health                               | Health check               | No   |
| POST   | /api/v1/check-ins                     | Submit daily check-in      | Yes  |
| GET    | /api/v1/check-ins/patients/{id}       | Check-in history           | Yes  |
| POST   | /api/v1/meals/analyze                 | Photo upload + AI analysis | Yes  |
| GET    | /api/v1/meals/patients/{id}           | Meal history               | Yes  |
| GET    | /api/v1/vitality/patients/{id}        | Current score + breakdown  | Yes  |
| GET    | /api/v1/vitality/patients/{id}/trends | 7/30-day trends            | Yes  |
| POST   | /api/v1/habits/activate               | Start a habit (max 3)      | Yes  |
| POST   | /api/v1/habits/{id}/complete          | Mark habit done today      | Yes  |
| GET    | /api/v1/habits/patients/{id}          | Active habits + streaks    | Yes  |
| GET    | /api/v1/insights/patients/{id}        | Personal AI insights       | Yes  |

### Data Model

```
users
  id (UUID, PK)
  email (VARCHAR, unique)
  hashed_password (VARCHAR)
  display_name (VARCHAR)
  patient_id (UUID, FK -> patients)
  created_at, updated_at

patients
  id (UUID, PK)
  fhir_resource (JSONB)
  created_at, updated_at

check_ins
  id (UUID, PK)
  patient_id (UUID, FK -> patients)
  sleep_quality (INTEGER, 1-5)
  energy_level (INTEGER, 1-5)
  mood (VARCHAR, enum)
  symptoms (TEXT, nullable)
  symptoms_structured (JSONB, nullable — AI-parsed)
  date (DATE, unique per patient)
  created_at

meals
  id (UUID, PK)
  patient_id (UUID, FK -> patients)
  photo_url (VARCHAR)
  analysis (JSONB — AI response: foods, highlights, score, tip)
  nutrition_score (INTEGER, 0-100)
  meal_type (VARCHAR — breakfast/lunch/dinner/snack)
  date (DATE)
  created_at

habits
  id (UUID, PK)
  patient_id (UUID, FK -> patients)
  template_id (VARCHAR — references habit library)
  name (VARCHAR)
  dimension (VARCHAR — nutrition/sleep/activity/mood)
  started_at (TIMESTAMP)
  is_active (BOOLEAN, default true)

habit_completions
  id (UUID, PK)
  habit_id (UUID, FK -> habits)
  completed_at (DATE, unique per habit)

vitality_scores
  id (UUID, PK)
  patient_id (UUID, FK -> patients)
  nutrition (INTEGER, 0-100)
  sleep (INTEGER, 0-100)
  activity (INTEGER, 0-100)
  mood (INTEGER, 0-100)
  overall (INTEGER, 0-100)
  calculated_at (TIMESTAMP)

insights
  id (UUID, PK)
  patient_id (UUID, FK -> patients)
  insight_text (TEXT)
  insight_type (VARCHAR — correlation/trend/recommendation)
  correlation_data (JSONB)
  generated_at (TIMESTAMP)

consents (reuse from Entre Deux)
audit_events (reuse from Entre Deux)
```

### Third-Party Dependencies

| Dependency                 | Purpose                                        | Risk                      | Alternative                  |
| -------------------------- | ---------------------------------------------- | ------------------------- | ---------------------------- |
| Mistral AI SDK             | All AI operations (analysis, vision, insights) | Medium — API availability | OpenAI/Anthropic as fallback |
| SQLAlchemy async + asyncpg | Database ORM                                   | Low — proven, stable      | Raw asyncpg                  |
| FastAPI                    | HTTP framework                                 | Low — proven              | None needed                  |
| passlib + python-jose      | Auth (bcrypt + JWT)                            | Low — standard libs       | None needed                  |
| React 19 + Vite            | Frontend framework                             | Low — proven              | None needed                  |
| vite-plugin-pwa            | PWA support                                    | Low — simple config       | Manual service worker        |

---

## 5. Edge Cases & Error Handling

| Scenario                                  | Expected Behavior                                                            | Priority |
| ----------------------------------------- | ---------------------------------------------------------------------------- | -------- |
| User submits 2 check-ins same day         | Server rejects with "Vous avez déjà complété votre bilan aujourd'hui"        | P0       |
| Meal photo is not food (selfie, document) | AI returns "Nous n'avons pas pu identifier de repas dans cette photo"        | P1       |
| Meal photo is blurry/dark                 | AI returns low-confidence analysis with "Essayez avec un meilleur éclairage" | P1       |
| Mistral API timeout (>30s)                | Return 504 with "Le service d'analyse est temporairement lent. Réessayez."   | P0       |
| Mistral API down                          | Return 502 with "Service d'analyse indisponible" + cached last-known score   | P0       |
| User has <3 days of data for score        | Show encouraging message instead of incomplete score                         | P0       |
| Habit streak broken after 20+ days        | Reset to 0 with extra encouragement, not punishment                          | P1       |
| JWT token expired                         | Silent refresh; if refresh fails, redirect to login                          | P0       |
| User accesses another user's data         | 403 Forbidden (patient isolation enforced)                                   | P0       |
| Large file upload (>10MB photo)           | Client-side rejection before upload with message                             | P1       |

### Security Considerations

- [ ] Input validation on all endpoints (Pydantic models with constraints)
- [ ] Patient data isolation enforced at middleware level (reuse from Entre Deux)
- [ ] SQL injection prevention via SQLAlchemy ORM (no raw SQL)
- [ ] CORS restricted to frontend origin (no wildcards)
- [ ] Rate limiting on auth (10/min) and AI endpoints (5/min)
- [ ] JWT secrets in environment variables only
- [ ] Meal photos stored securely (no public URLs without auth)
- [ ] Consent required for all AI-powered endpoints

---

## 6. Testing Strategy

### Unit Tests (Target: 80%+ coverage on business logic)

- [ ] VitalityScorer — score calculation with various data combinations
- [ ] Habit streak logic — increment, reset, edge cases (midnight, timezone)
- [ ] Check-in validation — duplicate prevention, data constraints
- [ ] Meal analysis parsing — structured output extraction from AI response
- [ ] Insight correlation — pattern detection algorithm
- [ ] Auth service — token generation, validation, refresh

### Integration Tests

- [ ] All 14 API endpoints (happy path + error cases)
- [ ] Auth flow: register -> login -> access protected endpoint -> refresh
- [ ] Check-in -> vitality recalculation pipeline
- [ ] Meal upload -> AI analysis -> score update pipeline
- [ ] Patient isolation: user A cannot access user B's data
- [ ] Consent enforcement: AI endpoints blocked without active consent

### E2E Tests (Critical Paths Only)

- [ ] Register -> first check-in -> see vitality score
- [ ] Login -> complete habit -> see streak update
- [ ] Meal photo upload -> see analysis result (with mocked AI)

### What NOT to Test

- Mistral AI response quality (external service, not our code)
- CSS/visual styling (manual review during polish phase)
- PWA installation flow (manual test on real device)
- Demo data seeder (run once, verify manually)

---

## 7. Milestones & Build Order

### Phase 1: Backend Foundation (Day 1-2, Apr 14-15)

- [ ] Project scaffold from Entre Deux template
- [ ] Database schema + Alembic migrations
- [ ] Auth system (register, login, refresh) — reuse from Entre Deux
- [ ] Health check endpoint
- [ ] Check-in endpoints (POST submit, GET history)
- [ ] CheckInAnalyzer agent (symptom structuring)
- [ ] Audit + consent middleware — reuse from Entre Deux
- [ ] CI pipeline (ruff + mypy + pytest)
- [ ] Unit + integration tests for auth + check-ins
- **Gate:** CI green, auth works, check-ins store and retrieve, 80%+ coverage

### Phase 2: Core Features (Day 3-5, Apr 16-18)

- [ ] Meal analysis endpoint + MealAnalyzer agent
- [ ] VitalityScorer service + endpoints (score, trends)
- [ ] Habit system (activate, complete, list with streaks)
- [ ] HabitRecommender agent
- [ ] InsightEngine agent + endpoint
- [ ] Score recalculation on new data
- [ ] Demo data seeder script (Marie's 30-day journey)
- [ ] Integration tests for all pipelines
- **Gate:** All 14 API endpoints working, all agents functional, demo data seeded, 80%+ coverage

### Phase 3: Frontend (Day 6-9, Apr 19-22)

- [ ] React scaffold + design system (warm earth tones, Lora/Inter, French)
- [ ] Check-in screen (the hero — must be perfect, <60s flow)
- [ ] Vitality Score screen (circular score + 4 dimensions + trend)
- [ ] Habits screen (3 cards + streaks + completion)
- [ ] Meals screen (camera + AI results + history)
- [ ] Insights screen (cards + locked state)
- [ ] Auth screens (login, register, welcome)
- [ ] Bottom navigation
- [ ] Error boundaries + loading states
- **Gate:** Full user flow works end-to-end, all screens in French, accessible

### Phase 4: Polish + Deploy (Day 10-11, Apr 23-24)

- [ ] Animation polish (score fill, streak flame, completion celebration)
- [ ] Mobile responsiveness pass on real phone
- [ ] Accessibility pass (contrast, touch targets, font sizes)
- [ ] Docker compose + Cloud Run deployment
- [ ] Seed demo data on production
- [ ] E2E tests on critical paths
- **Gate:** Production URL works, demo flow completes in <3 min, all tests pass

### Phase 5: Demo + Submit (Day 12-13, Apr 25-27)

- [ ] Demo video (2 min — Marie's story)
- [ ] Screenshots for application
- [ ] Demo script for live walkthrough
- [ ] Final application review
- [ ] Submit on Agorize
- **Gate:** Submitted before April 27 deadline

---

## 8. Out of Scope (Explicitly)

- NOT building: Voice check-ins (Voxtral) — revisit post-challenge
- NOT building: Push notification system — users set phone alarms
- NOT building: Customizable vitality weights — hardcoded for credibility
- NOT building: FHIR Consent management UI — backend enforcement only
- NOT building: Audit event browsing UI — backend logging only
- NOT building: Data export feature — post-challenge
- NOT building: Multi-language support — French only for now
- NOT building: Social/sharing features — post-challenge
- NOT building: Doctor dashboard — post-challenge
- NOT building: Nestle product recommendations — described in pitch, not in MVP
- Will revisit in v2: Step count integration (Health API), social accountability, doctor sharing, English support

---

## 9. Open Questions

- [x] Project location? → `C:\Users\pyaes\vitalage` (confirmed)
- [x] Reuse Entre Deux code? → Yes (confirmed)
- [ ] Meal photo AI accuracy on French food? → Test with Mistral vision during Phase 2; fallback to curated demo if <7/10 accuracy
- [ ] Where to store meal photos? → Cloud Run local storage for MVP (no S3/GCS needed for demo)
- [ ] Agorize form fields? → Need to check before Phase 1

---

## 10. Approval

- [ ] **PRD reviewed and understood** — I (Seon) confirm the requirements are clear
- [ ] **Architecture approved** — The technical approach makes sense
- [ ] **Scope locked** — No features will be added during build without updating this PRD

> **Once approved, this PRD becomes the source of truth. Every feature, every endpoint, every component traces back to a user story above. If it's not in the PRD, it's not getting built.**
