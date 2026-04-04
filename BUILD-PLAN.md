# VitalAge — Build Plan

## Deadline: April 27, 2026 (22 days remaining)

## Phase 1: Application (Apr 14-15)

- [ ] Log into Agorize, extract Nestle Vital form fields
- [ ] Draft application answers mapped to form
- [ ] Record video demo if required
- [ ] Submit application

## Phase 2: Backend MVP (Apr 16-19)

### Day 1: Project scaffold + check-in engine

- [ ] Initialize FastAPI project from Entre Deux template
- [ ] Database schema: users, check_ins, meals, habits, vitality_scores
- [ ] FHIR R5 models: Observation (check-in data), QuestionnaireResponse (daily check-in)
- [ ] `POST /api/v1/check-ins` — submit daily check-in (sleep, energy, mood, symptoms)
- [ ] `GET /api/v1/check-ins/patients/{id}` — list check-in history
- [ ] `CheckInAnalyzer` agent — structures free-text symptoms, detects patterns
- [ ] Auth endpoints (register, login, refresh)
- [ ] Tests

### Day 2: Meal analysis + nutrition scoring

- [ ] `MealAnalyzer` agent — Mistral vision analyzes meal photo for nutritional content
  - Identifies foods in image
  - Estimates nutritional profile (protein, fiber, vitamins, hydration)
  - Returns nutritional quality score (not calories)
  - Generates positive micro-tip ("great fiber, consider adding vitamin C source")
- [ ] `POST /api/v1/meals/analyze` — photo upload -> AI meal analysis
- [ ] `GET /api/v1/meals/patients/{id}` — meal history with nutrition profiles
- [ ] Nutrition scoring algorithm (Mediterranean diet adherence, nutrient diversity)
- [ ] Tests

### Day 3: Vitality score engine

- [ ] `VitalityScorer` service — composite algorithm:
  - Nutrition dimension (0-100): based on meal quality, nutrient diversity, consistency
  - Sleep dimension (0-100): based on reported sleep quality and duration
  - Activity dimension (0-100): based on reported activity (steps if available, self-report otherwise)
  - Mood dimension (0-100): based on mood check-ins, symptom frequency
  - Overall Vitality: weighted composite (configurable weights)
- [ ] `GET /api/v1/vitality/patients/{id}` — current vitality score + history
- [ ] `GET /api/v1/vitality/patients/{id}/trends` — weekly/monthly vitality trends
- [ ] Score recalculation on new check-in/meal data
- [ ] Tests

### Day 4: Micro-habit system + insights engine

- [ ] Habit template library (20+ evidence-based micro-habits):
  - Sleep: "Sleep before 11pm", "No screens 30 min before bed"
  - Nutrition: "Eat 1 fruit before noon", "Drink water with every meal"
  - Activity: "Walk 10 min after lunch", "Stretch for 5 min in morning"
  - Mood: "Write 1 thing you're grateful for", "Call a friend this week"
- [ ] `POST /api/v1/habits/activate` — start a new habit
- [ ] `POST /api/v1/habits/{id}/complete` — mark habit done today
- [ ] `GET /api/v1/habits/patients/{id}` — active habits with streaks
- [ ] Habit recommendation agent — selects habits based on weakest vitality dimension
- [ ] `InsightEngine` agent — detects correlations after 2+ weeks of data:
  - Sleep duration vs next-day energy
  - Meal nutrition vs afternoon mood
  - Activity vs sleep quality
  - Generates natural-language insights in French
- [ ] `GET /api/v1/insights/patients/{id}` — personalized AI insights
- [ ] Audit logging for all AI operations
- [ ] Integration tests for full pipeline

## Phase 3: Frontend MVP (Apr 20-24)

### Day 5: Check-in + Meal screens

- [ ] Project scaffold: React 19 + TypeScript + Tailwind + shadcn + PWA
- [ ] Design system: warm, inviting, accessible (larger text for 45-70 demographic)
- [ ] **Check-in screen** — morning ritual:
  - Sleep quality (1-5 tap buttons, large touch targets)
  - Energy level (1-5 tap buttons)
  - Mood (icon selection, not text)
  - Optional: symptoms/notes (free text or voice)
  - Submit animation with celebration (BJ Fogg: celebrate completion)
  - Total interaction time: <60 seconds
- [ ] **Meal screen** — meal photo capture
  - Camera capture with food framing guide
  - AI analysis result: nutritional highlights (positive framing)
  - Micro-tip display
  - Meal history gallery

### Day 6: Vitality Score + Habits screens

- [ ] **Vitality Score screen** — the centerpiece
  - Large circular score display (0-100) with color gradient
  - 4 dimension breakdown (nutrition, sleep, activity, mood)
  - Weekly trend sparkline
  - "Up 3 from last week" change indicator
  - Tap dimension for detail drill-down
- [ ] **Habits screen** — Duolingo-style
  - 3 active habits with streak flames
  - Tap to complete today
  - Progress ring for each habit
  - "Unlock new habit" teaser when all 3 have 7+ day streaks

### Day 7: Insights + Profile screens

- [ ] **Insights screen** — AI-generated personal correlations
  - Card-based layout, one insight per card
  - "When you sleep >7h, your energy next day is 40% higher"
  - Visual correlation charts (simple bar/line)
  - Locked state for first 2 weeks ("keep checking in to unlock insights")
- [ ] **Profile/Settings screen**
  - Personal info
  - Check-in reminder time setting
  - Vitality dimension weight customization (autonomy)
  - Data export
- [ ] Bottom navigation (Check-in, Meals, Vitality, Habits, Insights)

### Day 8-9: Polish + onboarding

- [ ] Onboarding flow:
  - Welcome + value proposition (3 swipe screens)
  - Implementation intention: "When will you check in?" (time picker)
  - Consent capture (FHIR Consent)
  - First check-in immediately after onboarding
- [ ] Error boundaries, loading states, offline banner
- [ ] Mobile responsiveness pass (primary device = phone)
- [ ] Accessibility pass (font sizes, contrast, touch targets for 45-70 demographic)
- [ ] Notification/reminder system for daily check-in
- [ ] Animation polish (score changes, streak celebrations)

## Phase 4: Deploy + Demo (Apr 24-26)

- [ ] Docker compose (backend + frontend + postgres)
- [ ] Deploy to Google Cloud Run
- [ ] Seed demo account with 30 days of simulated check-in data
  - Show score progression from 55 to 78
  - Show insight unlocking
  - Show habit streaks
- [ ] Demo walkthrough script
- [ ] Screenshots/video for application
- [ ] Final polish pass

## Phase 5: Submit (Apr 27)

- [ ] Final application review
- [ ] Submit on Agorize before deadline
- [ ] Celebrate (again)

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND (PWA)                     │
│  React 19 + TypeScript + Tailwind + shadcn           │
│                                                       │
│  Screens: Check-in | Meals | Vitality | Habits | Insights │
│  Auth: JWT tokens                                    │
│  State: useAsyncData hook                            │
│  Accessibility: 44px touch targets, 18px min font    │
└────────────────────┬────────────────────────────────┘
                     │ HTTPS
┌────────────────────▼────────────────────────────────┐
│                    BACKEND (FastAPI)                  │
│                                                       │
│  api/v1/                                             │
│    ├── auth.py          (register, login, refresh)    │
│    ├── check_ins.py     (submit, list)               │
│    ├── meals.py         (analyze photo, list)        │
│    ├── vitality.py      (score, trends)              │
│    ├── habits.py        (activate, complete, list)   │
│    ├── insights.py      (personal correlations)      │
│    └── consents.py      (FHIR consent management)    │
│                                                       │
│  agents/                                             │
│    ├── check_in_analyzer.py   (symptom structuring)  │
│    ├── meal_analyzer.py       (Mistral vision)       │
│    ├── insight_engine.py      (correlation detection) │
│    └── habit_recommender.py   (personalized selection)│
│                                                       │
│  services/                                           │
│    ├── check_in_service.py    (daily check-in logic) │
│    ├── meal_service.py        (meal analysis pipeline)│
│    ├── vitality_service.py    (score calculation)    │
│    ├── habit_service.py       (streak management)    │
│    ├── insight_service.py     (correlation analysis) │
│    └── audit_service.py       (FHIR AuditEvent)     │
│                                                       │
│  db/                                                 │
│    ├── models.py              (SQLAlchemy)            │
│    └── repositories/          (data access)          │
│                                                       │
│  middleware/                                         │
│    ├── auth.py                (JWT validation)       │
│    └── consent.py             (FHIR consent check)   │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│               PostgreSQL 16                          │
│  FHIR R5 JSONB: Observation, QuestionnaireResponse,  │
│  Consent, AuditEvent                                 │
│  + users, check_ins, meals, habits, habit_completions,│
│    vitality_scores, insights                         │
└─────────────────────────────────────────────────────┘
```

## Vitality Score Algorithm

```python
# Dimension scores (each 0-100)

nutrition_score = weighted_average(
    meal_quality_avg_7d,        # Average nutritional quality of meals (0-100)
    nutrient_diversity_7d,      # How many nutrient groups covered (0-100)
    meal_consistency_7d,        # Regular meals vs skipping (0-100)
)

sleep_score = weighted_average(
    sleep_quality_avg_7d,       # Self-reported 1-5 scaled to 0-100
    sleep_consistency_7d,       # Variance in sleep quality (lower = better)
)

activity_score = weighted_average(
    activity_self_report_7d,    # Self-reported activity level
    habit_completion_rate_7d,   # Activity-related habit streaks
)

mood_score = weighted_average(
    mood_avg_7d,                # Self-reported mood scaled to 0-100
    mood_stability_7d,          # Variance (lower = better)
    symptom_frequency_7d,       # Fewer symptoms = higher score
)

# Overall vitality (default weights, user-customizable)
vitality = (
    nutrition_score * 0.30 +
    sleep_score * 0.25 +
    activity_score * 0.25 +
    mood_score * 0.20
)
```

## What We Reuse from Entre Deux

| Component                     | Reuse Level | Notes                                                    |
| ----------------------------- | ----------- | -------------------------------------------------------- |
| FastAPI project structure     | 90%         | Same clean architecture                                  |
| Mistral utils                 | 100%        | safe_chat_complete, safe_json_parse                      |
| Journal agent patterns        | 70%         | Check-in analyzer similar to journal structuring         |
| Auth system (JWT)             | 100%        | Same middleware                                          |
| FHIR data model patterns      | 60%         | Observations for check-ins, new models for habits/scores |
| Audit logging                 | 100%        | Same FHIR AuditEvent pattern                             |
| Consent middleware            | 100%        | Same consent-first architecture                          |
| React + Tailwind + shadcn     | 90%         | Adapt design system for older demographic                |
| PWA configuration             | 100%        | Same vite-plugin-pwa                                     |
| Docker + Cloud Run            | 100%        | Same deployment                                          |
| useAsyncData hook             | 100%        | Same data fetching                                       |
| Error boundaries              | 100%        | Same crash resilience                                    |
| Voice transcription (Voxtral) | 80%         | For voice check-ins                                      |

## Micro-Habit Library (Initial 20)

### Sleep (5)

1. Sleep before 11pm
2. No screens 30 min before bed
3. Wake up at the same time daily
4. No caffeine after 2pm
5. Read for 10 min before sleep

### Nutrition (5)

1. Eat 1 fruit before noon
2. Drink a glass of water with every meal
3. Eat 1 serving of vegetables at lunch
4. Replace 1 processed snack with nuts
5. Eat breakfast within 1 hour of waking

### Activity (5)

1. Walk 10 min after lunch
2. Stretch for 5 min in morning
3. Take the stairs instead of elevator
4. Stand up every hour for 2 min
5. Walk 5000 steps today

### Mood/Wellbeing (5)

1. Write 1 thing you're grateful for
2. Call or message a friend
3. Spend 10 min outside in daylight
4. Take 5 deep breaths when stressed
5. Do one thing just for yourself today

## Risk Mitigation

| Risk                          | Mitigation                                                             |
| ----------------------------- | ---------------------------------------------------------------------- |
| Meal photo AI accuracy        | Start with quality scoring, not calorie counting (more forgiving)      |
| User fatigue at week 2-3      | Progressive complexity + insight rewards unlock at exactly this window |
| Competitive Foodvisor (Paris) | We're a companion, not a food database. Different product category     |
| "Just another wellness app"   | Vitality Score + personal correlations = unique differentiator         |
| Older demographic adoption    | Accessible-first UX, voice input option, larger touch targets          |
| 22-day timeline               | More time than VitaLens, reuse 80%+ from Entre Deux                    |
