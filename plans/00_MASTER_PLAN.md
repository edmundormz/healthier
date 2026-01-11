# CH Health OS — MVP Master Implementation Plan

**Goal:** Build and deploy MVP ASAP with production-ready foundation.

**Last Updated:** January 11, 2026, 10:53 AM CST  
**Current Phase:** Phase 1 - Foundation (95% complete)  
**Major Milestone:** ✅ API Routes Complete - 18 endpoints implemented and tested

---

## Tech Stack (Confirmed)

- **Frontend:** Next.js 14+ (App Router, PWA) → Vercel
- **Backend API:** FastAPI (Python 3.11+) with uvicorn → Render
- **Database:** Supabase (Postgres 15+)
- **ORM:** SQLAlchemy 2.0+ (type safety, easier for beginners)
- **AI/Agent:** LangGraph 0.2+ (latest stable)
- **Auth:** Supabase Auth
- **Bot:** Telegram Bot API
- **Timezone:** America/Chicago (CST)

**Note:** See `PROJECT_CONVENTIONS.md` for detailed standards and best practices.

---

## Architecture Decisions

### 1. State Management (LangGraph)
**Recommendation: Hybrid approach**

- **Conversation state:** Store in Supabase `conversation_sessions` table
  - session_id, user_id, context (JSONB), last_message_at, expires_at
  - Keep last 5-10 messages for context
  - Auto-expire after 1 hour of inactivity
- **Health state:** Lives in domain tables (routines, daily_snapshots, etc.)
- **LangGraph checkpointer:** Use PostgresSaver (LangGraph built-in)
  - Connects directly to Supabase
  - Handles workflow state persistence

**Why:** Simple, reliable, fully auditable. No Redis needed for MVP.

---

### 2. Cron Jobs & Scheduled Tasks
**Recommendation: Render Cron Jobs + Supabase Edge Functions**

**For AM/PM Briefs (time-critical):**
- Use Render Cron Jobs (native feature in Render)
- Hit FastAPI endpoint: `POST /api/internal/trigger-briefs`
- Schedule:
  - AM Brief: `0 7 * * *` (7 AM CST daily)
  - PM Recap: `0 20 * * *` (8 PM CST daily)

**For maintenance tasks:**
- Supabase pg_cron (lightweight tasks)
  - Daily snapshot generation
  - Expired routine cleanup
  - Streak calculations

**Why:** Render cron is simple, reliable, and included. No need for n8n in MVP.

---

### 3. Routine Versioning — Helper Patterns
**Recommendation: Service layer abstraction**

Create a `RoutineService` class with:

```python
class RoutineService:
    def get_active_items(self, user_id, moment_of_day, current_date):
        """Returns only active items for today"""
        # Handles version + expiration logic
        
    def get_next_expiring_items(self, user_id, days_ahead=7):
        """Preview upcoming expirations"""
        
    def transition_to_next_version(self, item_id):
        """Auto-transition when item expires"""
```

**Database views to simplify queries:**
```sql
CREATE VIEW active_routine_items AS
SELECT ri.*
FROM routine_items ri
JOIN routine_cards rc ON ri.routine_card_id = rc.id
JOIN routine_versions rv ON rc.routine_version_id = rv.id
WHERE 
  CURRENT_DATE >= rv.start_date
  AND (rv.end_date IS NULL OR CURRENT_DATE <= rv.end_date)
  AND (ri.expires_at IS NULL OR CURRENT_DATE <= ri.expires_at);
```

**Why:** Hides complexity, makes queries fast, keeps controller code clean.

---

## Implementation Phases

### Phase 1: Foundation (Week 1) - 🚧 95% Complete
**Goal:** Infrastructure + data layer

1. **Project setup** ✅ COMPLETE
   - ✅ Initialize FastAPI project structure
   - ⏳ Initialize Next.js project (App Router)
   - ✅ Set up Supabase connection
   - ✅ Configure environment variables

2. **Database schema** ✅ COMPLETE
   - ✅ Write SQL migrations (8 files)
   - ✅ Create tables with proper indexes (24 tables)
   - ✅ Set up RLS policies
   - ✅ Create helper views (4 views)
   - ✅ **MAJOR:** Refactored to SQLAlchemy ORM with full type safety
     - ✅ 11 models created (User, Family, Routine, Habit, etc.)
     - ✅ 20+ Pydantic schemas for API validation
     - ✅ Service layer (UserService, FamilyService)
     - ✅ Connection pooling configured
     - ✅ Comprehensive documentation (5 guides)

3. **Authentication** ⏳ PENDING
   - ⏳ Supabase Auth setup
   - ⏳ Telegram user linking
   - ⏳ JWT validation middleware

4. **Base API structure** ✅ COMPLETE
   - ✅ Health check endpoint
   - ✅ Database connection pool (asyncpg + pgbouncer)
   - ✅ Error handling middleware
   - ✅ Logging setup (structlog)
   - ✅ Test endpoint demonstrating ORM
   - ✅ Server running and tested

5. **API Routes** ✅ COMPLETE
   - ✅ Users API routes (8 endpoints) - CRUD + family management
   - ✅ Routines API routes (5 endpoints) - Full CRUD
   - ✅ Habits API routes (5 endpoints) - Full CRUD
   - ✅ Service layer complete (4 services)
   - ✅ All endpoints tested and working
   - ✅ Fixed pgbouncer compatibility issue
   - ✅ Router registration with error handling

**Deliverable:** ✅ Working API with 18 endpoints + database (test data pending)

**Next:** Authentication & Testing

---

### Phase 2: Rules Engine (Week 2)
**Goal:** Core health logic (no AI yet)

1. **Routine system**
   - RoutineService with expiration logic
   - CRUD endpoints
   - Active items query

2. **Habits tracking**
   - Daily check-ins
   - Streak calculation
   - Reset logic

3. **Scoring engine**
   - Daily score calculation (0-100)
   - Routine adherence %
   - Habit completion %
   - Exercise completion %

4. **Snapshot generator**
   - Daily snapshot creation
   - Aggregation logic
   - Family score calculation

**Deliverable:** Working rules engine + REST API

---

### Phase 3: Telegram Bot (Week 3)
**Goal:** Basic interaction without AI

1. **Bot setup**
   - Webhook configuration
   - Message operator
   - Command routing (/today, /done, /status)

2. **Static responses**
   - Command handlers
   - Inline keyboards
   - Quick actions

3. **Notification sender**
   - Send message to user
   - Format routines as messages
   - Handle Telegram rate limits

**Deliverable:** Working Telegram bot with basic commands

---

### Phase 4: LangGraph + Vita (Week 4)
**Goal:** Conversational AI layer

1. **LangGraph setup**
   - Install dependencies
   - PostgresSaver checkpointer
   - Basic workflow

2. **Vita agent**
   - System prompt implementation
   - Tool calling (get routines, mark done, etc.)
   - Response formatting

3. **Orchestrator**
   - Route message to Vita
   - Execute health tools
   - Return formatted response

4. **Brief generators**
   - AM Brief workflow
   - PM Recap workflow
   - Context building from daily data

**Deliverable:** Conversational Vita responding via Telegram

---

### Phase 5: Dashboard (Week 5-6)
**Goal:** PWA for visualization and configuration

1. **Basic layout**
   - Authentication
   - Dashboard home
   - Navigation

2. **Core views**
   - Today's routines
   - Habits tracker
   - Score display
   - Streaks visualization

3. **Configuration**
   - Routine builder
   - Exercise plan setup
   - Body metrics input

4. **PWA setup**
   - Manifest
   - Service worker
   - Offline support (basic)

**Deliverable:** Functional PWA dashboard

---

## Security Implementation

### 1. Data Encryption
- **At rest:** Supabase encrypts by default (AES-256)
- **In transit:** HTTPS everywhere
- **Sensitive fields:** Consider `pgcrypto` for extra-sensitive data (optional for MVP)

### 2. Telegram Webhook Security
```python
def verify_telegram_signature(request):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    secret = hashlib.sha256(token.encode()).digest()
    
    # Verify X-Telegram-Bot-Api-Secret-Token header
    # Or use telegram.Update.de_json() which validates automatically
```

### 3. Supabase RLS Policies
```sql
-- Users can only see their own data
CREATE POLICY "Users can view own data"
ON users FOR SELECT
USING (auth.uid() = id);

-- Family members can see family data
CREATE POLICY "Family members can view family data"
ON families FOR SELECT
USING (
  id IN (
    SELECT family_id FROM family_memberships 
    WHERE user_id = auth.uid()
  )
);
```

### 4. API Security
- Rate limiting: Use slowapi (FastAPI middleware)
- Input validation: Pydantic models
- CORS: Restrict to frontend domain
- Internal endpoints: Require API key header

---

## Project Structure

```
healthier/
├── backend/                 # FastAPI
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── routines.py
│   │   │   │   ├── habits.py
│   │   │   │   ├── telegram.py
│   │   │   │   └── internal.py
│   │   │   └── dependencies.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   │   ├── routine_service.py
│   │   │   ├── scoring_service.py
│   │   │   └── telegram_service.py
│   │   ├── agents/          # LangGraph
│   │   │   ├── vita.py
│   │   │   ├── orchestrator.py
│   │   │   └── tools.py
│   │   └── main.py
│   ├── migrations/          # Alembic or raw SQL
│   ├── tests/
│   ├── requirements.txt
│   └── render.yaml
│
├── frontend/                # Next.js
│   ├── app/
│   │   ├── (auth)/
│   │   ├── dashboard/
│   │   ├── routines/
│   │   ├── habits/
│   │   └── layout.tsx
│   ├── components/
│   ├── lib/
│   │   ├── supabase.ts
│   │   └── api.ts
│   ├── public/
│   ├── package.json
│   └── next.config.js
│
├── database/
│   ├── migrations/
│   │   ├── 001_initial_schema.sql
│   │   ├── 002_routines.sql
│   │   └── 003_rls_policies.sql
│   └── seeds/
│       └── dev_data.sql
│
├── design_docs/             # Existing
└── MASTER_PLAN.md          # This file
```

---

## Critical Decisions Made ✅

### 1. ORM Choice: SQLAlchemy
**Reasoning:**
- Type safety with IDE autocomplete
- Built-in SQL injection protection
- Easier for beginners to learn
- Better refactoring support
- Can optimize specific queries later if needed

**Trade-off:** Slight performance overhead vs raw SQL, but negligible for our use case.

### 2. Timeline: Full MVP with Dashboard
User needs dashboard for visualization and configuration (6-8 week timeline).

### 3. User Experience Level: Beginner
Teaching-first approach with detailed comments and explanations.

---

## Prerequisites Confirmed ✅

- ✅ Render account ready
- ✅ GitHub repository initialized
- ✅ OpenAI API key available
- ⏳ Supabase project (will be shared)
- ⏳ Telegram bot token (will be shared)

---

## Critical Setup Tasks

### 1. Telegram Bot Token
- User will provide token
- Store in: Render environment variable `TELEGRAM_BOT_TOKEN`

### 2. Supabase Access
- User will share MCP access
- Need: Project URL + anon key + service role key

### 3. Webhook URL
- Render will provide: `https://ch-health-api.onrender.com`
- Set as Telegram webhook: `POST https://api.telegram.org/bot<TOKEN>/setWebhook`

---

## Development Workflow

1. **Local development:**
   - Backend: `uvicorn app.main:app --reload`
   - Frontend: `npm run dev`
   - Database: Connect to Supabase (no local Postgres needed)

2. **Testing:**
   - Pytest for backend
   - Jest for frontend
   - Manual testing via Telegram (ngrok for local webhook)

3. **Deployment:**
   - Backend: Git push → Render auto-deploy
   - Frontend: Git push → Vercel auto-deploy
   - Database: Run migrations via Supabase dashboard or CLI

---

## Monitoring & Observability

1. **Logging:**
   - structlog (JSON format)
   - Render logs (centralized)
   - Store important events in `system_events` table

2. **Metrics to track:**
   - Message processing time
   - LangGraph execution duration
   - API endpoint latency
   - Daily active users
   - Adherence rates

3. **Error handling:**
   - Sentry (optional, add later)
   - Telegram admin notifications for critical errors
   - Graceful fallbacks (if LangGraph fails, send static message)

---

## Next Immediate Steps

1. **Create detailed database schema** (I'll create this)
2. **Set up backend project structure**
3. **Set up frontend project structure**
4. **Connect to Supabase via MCP**
5. **Create initial migrations**
6. **Deploy "hello world" to Render**

---

## Questions for You

1. **Do you have a Render account?** (If not, we'll create one)
2. **GitHub repo?** (Should we initialize git?)
3. **Supabase project already created?** (Or should we create it?)
4. **Any preferences for Python libraries?**
   - HTTP client: httpx (recommended)
   - ORM: SQLAlchemy or raw SQL?
   - Testing: pytest (recommended)

---

## Timeline Estimate (Aggressive but Realistic)

- **Week 1:** Foundation + database schema
- **Week 2:** Rules engine + scoring
- **Week 3:** Telegram bot (basic)
- **Week 4:** LangGraph + Vita
- **Week 5-6:** Dashboard
- **Week 7:** Testing + polish
- **Week 8:** Deploy MVP

**Can be faster if we skip dashboard for first release** (Telegram-only MVP).

---

## Risk Mitigation

1. **LangGraph complexity** → Start simple, iterate
2. **Routine versioning bugs** → Extensive testing with mock data
3. **Telegram rate limits** → Implement backoff, queue messages
4. **Timezone issues** → Use `pytz`, store all times in UTC, display in CST

---

Ready to start? 

**Recommendation: Let's begin with the detailed database schema, then set up the backend skeleton.**
