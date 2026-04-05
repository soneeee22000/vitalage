# VitalAge — Revised Build Plan (Post Stress-Test)

## Deadline: April 27, 2026

## Strategic Changes from Original Plan

### What we cut (saves ~4 days)

- Voice check-ins (Voxtral) — nice-to-have, not a differentiator
- FHIR Consent UI — keep backend consent enforcement, cut the user-facing consent management screen
- Notification/reminder system — tell users to set a phone alarm; build push notifications post-challenge
- Customizable vitality weights — hardcode the weights, remove user control (it weakens score credibility)
- Full onboarding flow with swipe screens — replace with a single welcome + first check-in
- Audit event browsing UI — keep backend audit logging, cut the frontend viewer
- Data export feature — post-challenge

### What we add (wins the competition)

- 5-day concierge pilot with real 45+ adults (before building anything)
- Meal photo AI validation on 10 French meals (before committing to scope)
- "Marie's 30-day journey" seeded demo narrative
- French language throughout the demo
- Bottoms-up market sizing slide
- Health-outcome-first Nestle value framing

### Feature Tiers

| Tier                 | Features                                                                                | Demo State                                  |
| -------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------- |
| **T1: Must ship**    | Check-in + Vitality Score + Micro-Habits                                                | Fully functional, French UI                 |
| **T2: Should ship**  | Meal photo analysis                                                                     | Works on 5-6 French meals                   |
| **T3: Seeded demo**  | AI Insights/correlations                                                                | Marie's 30-day data, pre-generated insights |
| **T4: Cut from MVP** | Voice input, consent UI, notifications, weight customization, data export, audit viewer | Mention on "roadmap" slide only             |

---

## Phase 0: Validate Before Building (Apr 5-10)

### Track A: Concierge Pilot (Apr 5-10)

Goal: Get one proof line for the application — "X of Y pilot users completed 5+ daily check-ins over 5 days"

- [ ] Create Google Form with 4 check-in questions:
  - Qualité du sommeil (1-5)
  - Niveau d'énergie (1-5)
  - Humeur (selection: Bien / Correct / Fatigué / Stressé / Autre)
  - Symptômes ou remarques? (optional free text)
- [ ] Recruit 5-8 adults aged 45+ (parents, neighbors, parents of friends, colleagues' parents)
  - Target: people who care about health but don't use fitness apps
  - Explain: "I'm testing a 60-second daily health check-in for a startup challenge — can you fill out a short form each morning for 5 days?"
- [ ] Send daily WhatsApp/SMS reminder at their chosen morning time
- [ ] Track completion in spreadsheet: who filled out, when, how long it took
- [ ] Day 5: Manually analyze each person's data, write them a personal insight:
  - "You had your best energy on days you reported sleeping 4-5/5"
  - "Your mood was most stable mid-week — weekend routines might differ"
- [ ] Day 6-7: Ask each participant 3 exit questions:
  - Was the daily check-in easy to maintain? (1-5)
  - Did the personal insight feel useful? (Y/N)
  - Would you use an app that did this automatically? (Y/N)
- [ ] Compile results into one application paragraph

### Track B: Meal Photo AI Validation (Apr 5-8)

Goal: Decide if meal photo analysis is T1 or T3

- [ ] Photograph or source images of 10 common French meals:
  1. Croque-monsieur
  2. Salade niçoise
  3. Ratatouille with bread
  4. Tartine with cheese and greens
  5. Pot-au-feu
  6. Quiche lorraine
  7. Steak-frites with salad
  8. Soupe de légumes with bread
  9. Omelette aux champignons
  10. Plateau de fromages with fruit
- [ ] Test Mistral vision API on each: "Analyze this meal's nutritional qualities. Focus on what's good (protein, fiber, vitamins, minerals, hydration) and one suggestion for improvement. Respond in French. Do not estimate calories."
- [ ] Score results: Sensible and helpful? (Y/N for each)
- [ ] Decision gate:
  - 7+/10 sensible → Meal AI is T1, build it fully
  - 4-6/10 sensible → Meal AI is T2, demo with curated examples only
  - <4/10 sensible → Meal AI is T3, show as seeded data in Marie's story
- [ ] If Mistral fails: test Foodvisor API free tier as fallback

---

## Phase 1: Application Submission (Apr 11-13)

- [ ] Log into Agorize, extract Nestle Vital form fields
- [ ] Rewrite APPLICATION-NESTLE.md with stress-test fixes:
  - Lead with health outcomes, not commercial opportunity
  - Include concierge pilot results
  - Bottoms-up market sizing (14M × 40% smartphone × 5% conversion = 280K)
  - Single business model: B2B2C via Nestle (others in appendix only)
  - Reframe vitality score: "perceived vitality anchored to WHO-5 Well-Being Index"
  - Add "Phase 2 with Nestle" slide: what we'd build with their resources
  - French meal photo demo results (if meal AI validated)
  - One-line pilot proof: "X of Y adults 50+ completed 5+ daily check-ins"
- [ ] Draft application answers mapped to Agorize form
- [ ] French-language pitch summary (even if form is English)
- [ ] Record 2-min video walkthrough if required
- [ ] Submit application

---

## Phase 2: Backend MVP (Apr 14-19) — 6 days

### Day 1 (Apr 14): Project scaffold + Auth

- [ ] Initialize FastAPI project from Entre Deux template
- [ ] Database schema (PostgreSQL):
  - users
  - check_ins (sleep_quality, energy_level, mood, symptoms, created_at)
  - meals (photo_url, analysis_json, nutrition_score, created_at)
  - habits (template_id, user_id, started_at)
  - habit_completions (habit_id, completed_at)
  - vitality_scores (user_id, nutrition, sleep, activity, mood, overall, calculated_at)
  - insights (user_id, insight_text, correlation_data, generated_at)
- [ ] Auth endpoints: register, login, refresh (reuse from Entre Deux)
- [ ] JWT middleware (reuse from Entre Deux)
- [ ] Health check endpoint
- [ ] Tests

### Day 2 (Apr 15): Check-in engine

- [ ] `POST /api/v1/check-ins` — submit daily check-in
  - sleep_quality (1-5), energy_level (1-5), mood (enum), symptoms (optional text)
  - Validates one check-in per user per day
- [ ] `GET /api/v1/check-ins/patients/{id}` — check-in history with pagination
- [ ] CheckInAnalyzer agent — structures free-text symptoms into categories
  - Reuse journal agent pattern from Entre Deux
  - Uses `mistral_utils.safe_chat_complete`
- [ ] Audit logging for AI calls (backend only, no UI)
- [ ] Tests

### Day 3 (Apr 16): Meal analysis (if validated in Phase 0)

If meal AI scored 7+/10:

- [ ] `POST /api/v1/meals/analyze` — photo upload + Mistral vision analysis
  - Returns: identified foods, nutritional highlights, quality score (0-100), micro-tip
  - Positive framing only, French language output
  - No calorie estimation — qualitative nutritional assessment
- [ ] `GET /api/v1/meals/patients/{id}` — meal history
- [ ] MealAnalyzer agent with structured output parsing
- [ ] Tests

If meal AI scored <7/10:

- [ ] Simplified meal endpoint that accepts manual meal description
- [ ] Pre-built responses for common French meal categories
- [ ] Focus remaining time on vitality score polish

### Day 4 (Apr 17): Vitality Score engine

- [ ] VitalityScorer service — composite algorithm:
  ```
  nutrition (30%): meal quality avg (7d) × 0.5 + meal consistency (7d) × 0.5
  sleep (25%): sleep quality avg (7d) × 0.7 + sleep consistency (7d) × 0.3
  activity (25%): habit completion rate (7d) × 0.6 + self-report (7d) × 0.4
  mood (20%): mood avg (7d) × 0.6 + mood stability (7d) × 0.2 + symptom frequency (7d) × 0.2
  overall = weighted sum (hardcoded weights, no user customization)
  ```
- [ ] `GET /api/v1/vitality/patients/{id}` — current score + dimension breakdown
- [ ] `GET /api/v1/vitality/patients/{id}/trends` — 7-day rolling scores
- [ ] Score auto-recalculation on new check-in or meal data
- [ ] Tests

### Day 5 (Apr 18): Micro-habit system

- [ ] Habit template library (12 evidence-based micro-habits, not 20):
  - Sleep (3): Sleep before 23h, No screens 30 min before bed, Wake at same time
  - Nutrition (3): 1 fruit before noon, Water with every meal, 1 vegetable serving at lunch
  - Activity (3): Walk 10 min after lunch, Stretch 5 min in morning, 5000 steps today
  - Mood (3): 1 gratitude note, 10 min outside in daylight, Call a friend this week
- [ ] `POST /api/v1/habits/activate` — start a habit (max 3 active)
- [ ] `POST /api/v1/habits/{id}/complete` — mark done today
- [ ] `GET /api/v1/habits/patients/{id}` — active habits with streak counts
- [ ] HabitRecommender agent — suggests habits targeting weakest vitality dimension
- [ ] Tests

### Day 6 (Apr 19): Insights engine + demo data seeder

- [ ] InsightEngine agent — detects correlations from 2+ weeks of data:
  - Sleep duration vs next-day energy
  - Meal quality vs afternoon mood
  - Habit completion vs dimension scores
  - Outputs natural-language insight in French
- [ ] `GET /api/v1/insights/patients/{id}` — personalized insights
- [ ] **Demo data seeder script** — creates "Marie, 58, Lyon" account with:
  - 30 days of check-in data showing progression
  - Vitality score climbing from 52 to 76
  - 3 active habits with realistic streaks (some missed days)
  - 5 pre-generated insights with real correlations
  - 15 meal analyses (if meal AI is T1)
- [ ] Integration tests for full pipeline
- [ ] Backend API documentation

---

## Phase 3: Frontend MVP (Apr 20-24) — 5 days

### Day 7 (Apr 20): Scaffold + Design System + Check-in

- [ ] React 19 + TypeScript + Tailwind + shadcn + PWA (vite-plugin-pwa)
- [ ] Design system setup:
  - Warm earth tones + vitality green (from CLAUDE.md design system)
  - Lora (headings) + Inter (body) via next/font/google equivalent
  - 18px minimum body font, 44px minimum touch targets
  - All text in French
- [ ] **Check-in screen** (the hero screen — must be perfect):
  - "Bonjour Marie" greeting with date
  - Sleep quality: 5 large tap buttons (1-5) with sleep icons
  - Energy level: 5 large tap buttons with energy icons
  - Mood: 5 icon selections (Bien, Content, Neutre, Fatigué, Stressé)
  - Optional symptoms text field
  - Submit with celebration animation
  - "Votre série: 12 jours" streak counter
  - Total interaction: under 60 seconds

### Day 8 (Apr 21): Vitality Score + Meal screens

- [ ] **Vitality Score screen** (the centerpiece):
  - Large circular score (0-100) with animated fill
  - 4 dimension bars: Nutrition (green), Sommeil (blue), Activité (orange), Humeur (purple)
  - "+3 depuis la semaine dernière" change indicator
  - 7-day trend sparkline
  - All labels in French
- [ ] **Meal screen** (if meal AI is T1/T2):
  - Camera capture button
  - AI analysis result card: nutritional highlights + micro-tip
  - Meal history gallery with nutrition scores
  - If T2: works but only demoed with pre-tested French meals

### Day 9 (Apr 22): Habits + Insights screens

- [ ] **Habits screen** (Duolingo-style):
  - 3 active habit cards with streak flame icons (Lucide, not emoji)
  - Tap to complete today — satisfying checkmark animation
  - Progress ring showing streak length
  - "Recommandé pour vous" suggestion from AI when slot opens
- [ ] **Insights screen**:
  - Card-based layout, one insight per card
  - Simple bar chart showing correlation visually
  - Locked state for new users: "Continuez vos bilans pour débloquer vos insights personnels"
  - For demo: Marie's 5 insights with visualizations

### Day 10 (Apr 23): Navigation + Auth + Polish

- [ ] Bottom navigation: Bilan | Repas | Vitalité | Habitudes | Insights
- [ ] Login / Register screens (minimal, functional)
- [ ] Simple welcome screen (single page, no multi-swipe onboarding):
  - "60 secondes par jour pour comprendre votre vitalité"
  - "Commencer" button -> register -> first check-in
- [ ] Error boundaries + loading states
- [ ] Mobile responsiveness pass (phone is primary device)
- [ ] Accessibility pass: contrast ratios 4.5:1+, all interactive elements have aria labels

### Day 11 (Apr 24): Demo flow + Animation polish

- [ ] "Marie's Journey" demo walkthrough:
  - Login as Marie -> see her 30-day vitality trajectory
  - Show score progression 52 → 76
  - Show her 3 habits with streaks
  - Show her 5 personal insights
  - Show a meal analysis (if T1/T2)
  - Do a live check-in as Marie
- [ ] Animation polish:
  - Score circle fill animation on load
  - Streak flame flicker
  - Check-in submit celebration
  - Dimension bar animations
- [ ] PWA install prompt + offline banner
- [ ] Test full demo flow 3 times end-to-end

---

## Phase 4: Deploy + Demo Prep (Apr 25-26) — 2 days

### Day 12 (Apr 25): Deploy

- [ ] Docker compose: backend + frontend + PostgreSQL
- [ ] Deploy to Google Cloud Run
- [ ] Run demo data seeder on production
- [ ] Verify full demo flow on production URL
- [ ] Test on actual phone (not just browser dev tools)
- [ ] Test on a second phone (borrow one — different screen size)

### Day 13 (Apr 26): Demo materials

- [ ] 2-minute demo video:
  - "Meet Marie, 58, retired teacher in Lyon"
  - Show her morning check-in (60 seconds)
  - Show her vitality score climbing over 30 days
  - Show her personal insights
  - Show a meal photo analysis (if T1)
  - End with: "Built in 22 days by one engineer. Imagine what Nestle Vital could do with this."
- [ ] Screenshots for application (phone-frame mockups)
- [ ] Demo script for live walkthrough (if needed at finalist stage)
- [ ] Final application review — all fields complete, all links working

---

## Phase 5: Submit (Apr 27)

- [ ] Final read-through of application
- [ ] Verify production URL is live and demo account works
- [ ] Submit on Agorize
- [ ] Backup: export all application answers locally

---

## Architecture (Simplified)

```
┌───────────────────────────────────────────────┐
│              FRONTEND (PWA)                     │
│  React 19 + TypeScript + Tailwind + shadcn     │
│                                                 │
│  Screens: Bilan | Repas | Vitalité |           │
│           Habitudes | Insights                  │
│  Auth: JWT          State: useAsyncData        │
│  Language: French   Font: 18px+ body           │
└──────────────────┬────────────────────────────┘
                   │ HTTPS
┌──────────────────▼────────────────────────────┐
│              BACKEND (FastAPI)                  │
│                                                 │
│  api/v1/                                       │
│    auth.py, check_ins.py, meals.py,            │
│    vitality.py, habits.py, insights.py         │
│                                                 │
│  agents/                                       │
│    check_in_analyzer.py, meal_analyzer.py,     │
│    insight_engine.py, habit_recommender.py     │
│                                                 │
│  services/                                     │
│    vitality_service.py, habit_service.py,      │
│    insight_service.py, audit_service.py        │
│                                                 │
│  db/ models.py + repositories/                 │
└──────────────────┬────────────────────────────┘
                   │
┌──────────────────▼────────────────────────────┐
│            PostgreSQL 16                       │
│  users, check_ins, meals, habits,              │
│  habit_completions, vitality_scores, insights  │
└───────────────────────────────────────────────┘
```

## Risk Register (Revised)

| Risk                                    | Likelihood | Impact | Mitigation                                                                                                                                                 |
| --------------------------------------- | ---------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Meal photo AI inaccurate on French food | Medium     | High   | Phase 0 validation gate; fallback to curated demos                                                                                                         |
| No pilot participants found in time     | Low        | High   | Ask parents, neighbors, friends' parents; even 3 people is enough                                                                                          |
| Backend takes longer than 6 days        | Medium     | Medium | Reusing 80%+ from Entre Deux; habits + insights are the only net-new services                                                                              |
| Frontend polish insufficient            | Medium     | Medium | Focus on 3 screens (check-in, vitality, habits); insights can be simpler                                                                                   |
| Demo data doesn't tell compelling story | Low        | High   | Write Marie's narrative FIRST, then generate data to match                                                                                                 |
| Judge asks about clinical validation    | High       | Medium | "Perceived vitality is anchored to WHO-5 Well-Being Index — a validated self-report instrument. We measure what predicts behavior change, not biomarkers." |
| "Why should we trust a solo founder?"   | High       | Medium | "One engineer, 207 tests, production-deployed predecessor. I know what I need next: a nutritionist and a UX researcher for the 50+ demographic."           |

## What Winning Looks Like

The judges should walk away thinking:

1. **"This person understands behavior change."** — The science is real, not buzzwords.
2. **"This could actually work for our customers."** — Marie's story makes it tangible.
3. **"This is already built."** — Live demo, not mockups.
4. **"Nestle Vital's name belongs on this."** — The B2B2C model is obvious.
5. **"One person built this? Imagine a team."** — Execution credibility.
