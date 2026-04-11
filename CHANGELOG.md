# Changelog

All notable changes to VitalAge are documented here.

## [0.1.0] - 2026-04-11

### Added

- Public landing page at `/bienvenue` with product overview, feature showcase, and demo CTA
- Demo account auto-fill on login page (Marie Dupont profile)
- Meal photo analysis with Mistral Vision AI
- AI-generated personal health insights (correlation detection)
- Demo data seeder with 30 days of realistic health data
- Production deployment on Google Cloud Run (europe-west1)
- Multi-stage Docker build (frontend compiled into backend static)

### Fixed

- DateTime timezone handling for all database columns
- Auto-create tables on startup for fresh deployments
- Graceful degradation when Mistral API key is missing

## [0.0.1] - 2026-04-10

### Added

- T1 MVP: daily check-in, vitality score dashboard, micro-habits
- 4-dimension vitality scoring (nutrition 30%, sleep 25%, activity 25%, mood 20%)
- 12 evidence-based habit templates across 4 dimensions
- Streak tracking with Duolingo-style gamification
- JWT authentication with user data isolation
- FHIR R5 data model compliance
- Audit logging for all AI agent calls
- React 19 PWA with mobile-first design
- Accessibility-first UI for 45-70 demographic (44px+ touch targets, 18px+ fonts)
- 64 tests (34 backend pytest + 30 frontend vitest)
- CI/CD pipeline (GitHub Actions + Google Cloud Build)
