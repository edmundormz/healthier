# CH Health OS

Private, family-centered health operating system built with rules-first AI assistance.

---

## Project Status

**Phase:** Frontend Complete - Ready for Testing & Deployment  
**Design:** ✅ Complete  
**Implementation:** 🚧 85% complete  
**Frontend:** ✅ Complete (Next.js 16 with Full CRUD)  
**Backend:** ✅ 95% complete (API ready, deployment pending)

**👉 See [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) for detailed progress**

---

## Quick Links

- **[Master Plan](plans/00_MASTER_PLAN.md)** — Complete implementation strategy
- **[Getting Started](GETTING_STARTED.md)** — Setup instructions
- **[Project Conventions](PROJECT_CONVENTIONS.md)** — Coding standards & best practices
- **[Database Schema](database/schema/DATABASE_SCHEMA.md)** — Complete data model
- **[Design Docs](design_docs/)** — Product & system documentation

---

## Architecture

```
┌─────────────────┐
│   Telegram Bot  │  ← Primary interface (Vita)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI (API)  │  ← Python backend (Render)
│   + LangGraph   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Supabase     │  ← Postgres + Auth
│   (Database)    │
└─────────────────┘
```

---

## Tech Stack

- **Backend:** FastAPI (Python 3.11+)
- **AI:** LangGraph + OpenAI
- **Database:** Supabase (Postgres)
- **Bot:** Telegram Bot API
- **Frontend:** Next.js 16.1.1 (PWA) ✅ Complete
- **Deploy:** Render (API), Vercel (Frontend)

---

## Core Features (MVP)

- ✅ Routine Builder with expiration logic
- ✅ Habits tracking with streaks
- ✅ Exercise planning (goal-aligned)
- ✅ Daily scoring & gamification
- ✅ Family momentum tracking
- ✅ Lifestyle-based rewards
- ✅ AM Brief & PM Recap via Telegram
- ✅ Vita conversational agent

---

## Project Structure

```
healthier/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/         # REST endpoints
│   │   ├── services/    # Business logic
│   │   ├── agents/      # LangGraph (Vita)
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/            # Next.js 16.1.1 ✅ Complete
│
├── database/
│   ├── schema/          # Schema documentation
│   └── migrations/      # SQL migrations
│
└── design_docs/         # Product documentation
    ├── README.md
    ├── 01_product_charter.md
    ├── 02_mvp_scope_and_features.md
    └── ...
```

---

## Getting Started

See **[GETTING_STARTED.md](GETTING_STARTED.md)** for detailed setup instructions.

### Quick Start (Local Development)

```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run API
uvicorn app.main:app --reload

# API will be available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

---

## Development Roadmap

### Phase 1: Foundation (Week 1)
- [x] Design documentation
- [x] Database schema
- [ ] Project setup
- [ ] Initial migrations
- [ ] Deploy to Render

### Phase 2: Rules Engine (Week 2)
- [ ] Routine service
- [ ] Habits service
- [ ] Scoring engine
- [ ] REST API endpoints

### Phase 3: Telegram Bot (Week 3)
- [ ] Webhook handler
- [ ] Command routing
- [ ] Static responses
- [ ] Notification system

### Phase 4: LangGraph + Vita (Week 4)
- [ ] LangGraph setup
- [ ] Vita agent
- [ ] Tool integration
- [ ] Brief generators

### Phase 5: Dashboard (Week 5-6) - ✅ Complete
- [x] Next.js 16.1.1 setup ✅
- [x] Authentication (Supabase Auth) ✅
- [x] Core views (dashboard, routines, habits, profile) ✅
- [x] Complete CRUD operations ✅
- [x] Forms with validation ✅
- [x] Delete functionality ✅
- [x] Loading states and error handling ✅
- [ ] PWA configuration (optional enhancement)

---

## Core Principles

1. **Rules > AI** — AI assists, doesn't decide
2. **Adherence > Optimization** — Consistency over perfection
3. **Traceability** — Health decisions must be explainable
4. **Low Friction** — Daily usage must be effortless
5. **Family First** — Shared momentum, not pressure

---

## Documentation

### Product Documentation
- [Why CH Health](design_docs/00_why_ch_health.md)
- [Product Charter](design_docs/01_product_charter.md)
- [MVP Scope](design_docs/02_mvp_scope_and_features.md)
- [Routines & Expiration](design_docs/03_routines_and_expiration_model.md)
- [Exercise System](design_docs/04_exercise_system.md)
- [Gamification](design_docs/05_gamification_and_rewards.md)

### Technical Documentation
- [Telegram Architecture](design_docs/06_telegram_and_vita_architecture.md)
- [Data Schema](design_docs/07_data_schema_v0.md)
- [LangGraph Orchestration](design_docs/08_langgraph_orchestration.md)

### Design Documentation
- [Visual Design](design_docs/10_visual_design_and_brand_direction.md)
- [Vita Personality](design_docs/11_vita_personality_and_voice.md)
- [Future Roadmap](design_docs/09_future_stages_and_roadmap.md)

---

## Environment Variables

See `.env.example` for required environment variables.

Key variables:
- `SUPABASE_URL` — Supabase project URL
- `SUPABASE_SERVICE_KEY` — Service role key
- `TELEGRAM_BOT_TOKEN` — Telegram bot token
- `OPENAI_API_KEY` — OpenAI API key for LangGraph

---

## Contributing

This is a private project for Family CH.

---

## License

Private — All rights reserved

---

## Contact

For questions or support, contact the development team.
