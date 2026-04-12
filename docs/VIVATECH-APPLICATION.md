# VitalAge — Nestle Vital VivaTech 2026 Application

**Challenge:** Holistic Well Being — The Smart Aging Companion Challenge
**Deadline:** May 4, 2026
**Apply at:** https://challenges.vivatech.com/en/challenges/nestle-vital-2026

---

## Company Information

- **Company Name:** Ekkhara
- **Type:** AI Venture Studio
- **Founded:** 2026
- **Employees:** 1
- **Location:** Paris, France
- **Website:** https://vitalage-102991984200.europe-west1.run.app/bienvenue

## Founder

- **Name:** Pyae Sone (Seon)
- **Role:** Founder & Full-Stack AI Engineer
- **Education:** Dual Master's — Telecom SudParis (France) + Asian Institute of Technology (Thailand)
- **Experience:** Former Founding AI Engineer at Siloett.AI (Station F accelerator)
- **LinkedIn:** [Update with your LinkedIn URL]

---

## Solution Name

**VitalAge** — Your daily vitality companion for smart aging

## One-Line Pitch

VitalAge turns 60 seconds of daily check-ins into a personal health equation, helping adults 45+ build sustainable micro-habits in nutrition, sleep, activity, and mood.

## Problem Statement (What pain point do you solve?)

Health apps fail older adults. 80% of health apps have under 6% retention at day 30. The reason: no feedback loop. Users log food — nothing happens. They track mood — nothing changes. Meanwhile, France has 14M+ adults over 60 (growing to 20M by 2030), and no accessible digital health companion serves this demographic without requiring expensive hardware or complex onboarding.

The core challenge is not tracking — it's adherence. People know what to do, they just don't stick to it. Existing solutions focus on data collection, not behavior change.

## Solution Description (How does your product work?)

VitalAge closes the feedback loop with 5 integrated features designed around behavior change science:

1. **Morning Check-in (60 seconds):** Sleep quality, energy level, mood, and optional symptoms — structured as a daily ritual, not a chore. AI structures free-text symptoms into actionable categories.

2. **Vitality Score (0-100):** A composite score across 4 dimensions — Nutrition (30%), Sleep (25%), Activity (25%), Mood (20%). Like a credit score for health: simple, tangible, and motivating. Recalculated in real-time with every new data point.

3. **Micro-Habits (Duolingo-style):** 3 active habits at a time, selected from 12 evidence-based templates. Streak tracking with celebration animations. Small wins compound into lasting change.

4. **Meal Photo Analysis:** Users photograph meals, and AI provides instant nutritional feedback — always positive framing (quality, not calories). Powered by Mistral Vision, a European AI model ensuring EU data residency.

5. **Personal AI Insights:** After 7+ days of data, the system detects personal correlations: "When you sleep 4+/5, your energy is 40% higher the next day." These are not generic tips — they are patterns from the user's own data.

## Behavior Change Science

VitalAge implements 5 peer-reviewed frameworks:

- **BJ Fogg Tiny Habits:** 60-second check-in anchored to morning routine
- **Nir Eyal Hook Model:** Trigger (morning) -> Action (check-in) -> Reward (score update) -> Investment (growing data history)
- **Self-Determination Theory:** Autonomy (choose your habits), Competence (watch your score improve), Relatedness (share milestones)
- **Implementation Intentions:** Onboarding asks "When will you check in?" to anchor the habit
- **JITAI (Just-In-Time Adaptive Interventions):** Right nudge at right moment based on the user's own patterns

## Target Audience

Adults 45-70 in France, starting with:

- Active retirees seeking preventive health tools
- Pre-retirees wanting to build healthy aging habits early
- Caregivers tracking vitality for family members

## Accessibility & Design

Built for the 45-70 demographic with accessibility-first principles:

- 44px+ touch targets (most are 56px)
- 18px minimum body font
- 4.5:1+ contrast ratio on all interactive elements
- French language throughout
- Progressive Web App — installable on any phone without app store
- Warm, inviting design system (not clinical, not sporty)

## Technology

| Layer           | Technology                              | Why                                   |
| --------------- | --------------------------------------- | ------------------------------------- |
| Frontend        | React 19, TypeScript, Tailwind CSS, PWA | Installable, mobile-first, accessible |
| Backend         | Python 3.12, FastAPI, SQLAlchemy async  | Async AI calls, type-safe             |
| Database        | PostgreSQL 16                           | FHIR R5 JSONB, reliable               |
| AI              | Mistral Small + Mistral Vision          | European AI, EU data residency        |
| Health Standard | FHIR R5                                 | Medical-grade data portability        |
| Infrastructure  | Google Cloud Run (europe-west1)         | Auto-scaling, EU-hosted               |

## Key Differentiators

1. **Feedback loop, not just tracking:** Every input generates immediate, personalized output
2. **European AI stack:** Mistral models ensure EU data residency — no data leaves Europe
3. **FHIR R5 compliance:** Health data stored in medical-standard format, portable to any healthcare system
4. **Adherence by design:** 60-second ritual, not a 10-minute chore — retention through simplicity
5. **Positive framing only:** Never counts calories, never judges — focuses on quality and progress
6. **No hardware required:** PWA works on any smartphone, no wearable needed

## Viability & Scalability

- **No app store friction:** PWA installable from browser — zero download barrier for older users
- **Low infrastructure cost:** Cloud Run scales to zero when idle, pays only for usage
- **Multi-language ready:** Architecture supports localization (French first, expandable)
- **API-first design:** 15 RESTful endpoints, ready for third-party integrations
- **Nestle Vital integration potential:** Nutrition dimension can incorporate Nestle Vital product recommendations, meal pairing suggestions, and nutritional supplement tracking

## Measurable Outcomes

Demo user Marie Dupont's 30-day journey:

- Vitality Score: 52 -> 76 (+46% improvement)
- Longest streak: 12 days consecutive
- Meals analyzed: 15 (with nutritional improvement trend)
- Active habits maintained: 3 simultaneous
- Check-in adherence: 93% (28/30 days)

## Live Demo

- **Landing Page:** https://vitalage-102991984200.europe-west1.run.app/bienvenue
- **Demo Account:** marie.dupont@demo.vitalage.health / vitalage2026
- **API Documentation:** https://vitalage-102991984200.europe-west1.run.app/docs
- **Source Code:** https://github.com/soneeee22000/vitalage

## Roadmap (Post-VivaTech)

**Q3 2026:** Voice check-ins (Voxtral), family dashboard, push notifications
**Q4 2026:** Nestle Vital product integration, pharmacist partnership pilot
**Q1 2027:** Clinical validation study, insurance partner pilot
**Q2 2027:** Multi-language rollout (DE, ES, IT), B2B2C model for senior residences

---

## Video Pitch Script (if required, 2 minutes)

[Opening — 15s]
"You have 14 million reasons to care about smart aging in France. But the average health app is abandoned in 7 days. VitalAge changes that."

[Problem — 20s]
"Health apps fail because they collect data without giving anything back. No feedback loop. No reason to come back tomorrow. For adults over 45, the problem is not information — it's adherence."

[Solution — 40s]
"VitalAge is a 60-second daily ritual. Check in each morning — sleep, energy, mood. Photograph your meals. Watch your Vitality Score evolve across 4 dimensions. Build 3 micro-habits with streaks. And after a week, discover personal insights: when YOU do X, YOU feel Y. It's your body's user manual, written by your own data."

[Demo — 20s]
"Let me show you Marie's journey. In 30 days, her Vitality Score went from 52 to 76. She maintained a 12-day streak. And she discovered that sleeping before 11pm boosted her energy by 40%."

[Tech — 15s]
"Built on European AI — Mistral models, EU data residency. FHIR R5 medical data standard. PWA — no app store, works on any phone. Scales to millions on Google Cloud."

[Ask — 10s]
"VitalAge is live today. We're looking for a partner to bring preventive health to 14 million French adults. Nestle Vital is that partner."
