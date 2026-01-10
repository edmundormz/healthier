# CH Health OS

Private, family-centered health operating system.

CH Health OS is a rules-first, AI-assisted system designed to support
daily health adherence, long-term consistency, and preventive care
for Candy, Héctor, and Family CH.

This repository contains the **design, product, and system documentation**
that defines the foundation of the platform before implementation.

---

## Purpose

CH Health OS exists to transform health from an occasional effort
into a sustainable daily operating system.

It prioritizes:
- Adherence over optimization
- Clarity over complexity
- Family momentum over individual pressure
- Prevention over reaction

---

## Documentation Structure

All design and product documentation lives in:


### Core Context & Philosophy

- `00_why_ch_health.md`  
  Reason of being. Context, motivation, and long-term vision.

- `01_product_charter.md`  
  Product purpose, principles, target users, and success metrics.

---

### MVP Definition

- `02_mvp_scope_and_features.md`  
  MVP scope, included features, and explicit out-of-scope items.

- `03_routines_and_expiration_model.md`  
  Routine system design, including time-bound and expiring protocols.

- `04_exercise_system.md`  
  Exercise planning aligned to individual goals.

- `05_gamification_and_rewards.md`  
  Scoring, streaks, family momentum, and lifestyle-based rewards.

---

### System Architecture

- `06_telegram_and_vita_architecture.md`  
  Telegram integration, Vita agent, and message flow.

- `07_data_schema_v0.md`  
  Core data model and tables for MVP.

- `08_langgraph_orchestration.md`  
  Agent architecture and orchestration (Orchestrator + Vita).

---

### Future & Design Direction

- `09_future_stages_and_roadmap.md`  
  Planned evolution from MVP to biometric and preventive stages.

- `10_visual_design_and_brand_direction.md`  
  Visual identity, UI principles, and luxury medical spa aesthetic.

- `11_vita_personality_and_voice.md`  
  Vita’s personality, tone, language rules, and conversational guardrails.

---

## Architecture Overview (Implementation Target)

- **Frontend:** Next.js (PWA)
- **Backend:** Next.js API routes
- **Database:** Postgres (Supabase recommended)
- **AI Layer:** LangGraph
  - Health Orchestrator (rules-first)
  - Vita (conversation & UX agent)
- **Notifications & Interaction:** Telegram Bot

---

## Core Principles

- Rules-first. AI assists, not decides.
- Health logic must be traceable and explainable.
- Daily usage must be low-friction.
- Gamification must feel elegant, not childish.
- Silence is respected. No noisy systems.

---

## Status

**MVP v0 — Design phase complete**  
Ready for implementation.

Next steps:
- Repository structure
- API contracts
- First LangGraph workflows
- Vita system prompt implementation
