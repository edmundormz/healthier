# Getting Started — Immediate Next Steps

This document outlines the exact steps to begin building CH Health OS MVP.

---

## Prerequisites Checklist

### Accounts & Services
- [ ] Render account (sign up at render.com)
- [ ] GitHub account
- [ ] Supabase project (or we'll create it)
- [ ] Telegram bot created (or we'll create it)
- [ ] Vercel account (optional for now, can add later)

### Tools Needed
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed (for frontend later)
- [ ] Git installed
- [ ] Code editor (VS Code recommended)
- [ ] Supabase CLI (optional but helpful)

---

## Phase 1A: Initial Setup (Day 1)

### Step 1: Initialize Git Repository
```bash
cd c:\Users\HectorRamirez\Desktop\Sandbox\healthier

# Initialize git
git init

# Create .gitignore
```

### Step 2: Set Up Backend Project Structure
```bash
# Create backend directory structure
mkdir -p backend/app/api/routes
mkdir -p backend/app/core
mkdir -p backend/app/models
mkdir -p backend/app/schemas
mkdir -p backend/app/services
mkdir -p backend/app/agents
mkdir -p backend/tests
mkdir -p backend/migrations
```

### Step 3: Create Backend Dependencies
Create `backend/requirements.txt`:
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0

# Database
psycopg2-binary==2.9.9
sqlalchemy==2.0.25
asyncpg==0.29.0

# Supabase
supabase==2.3.0

# LangGraph
langgraph==0.2.0
langchain==0.1.0
langchain-openai==0.0.5

# Telegram
python-telegram-bot==20.7

# HTTP
httpx==0.26.0

# Utilities
python-dotenv==1.0.0
python-multipart==0.0.6
pytz==2023.3

# Logging
structlog==24.1.0

# Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.26.0
```

### Step 4: Create Environment Configuration
Create `backend/.env.example`:
```
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_role_key

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_WEBHOOK_SECRET=generate_random_secret

# OpenAI (for LangGraph)
OPENAI_API_KEY=your_openai_key

# App Settings
ENVIRONMENT=development
DEBUG=true
TIMEZONE=America/Chicago

# API
API_HOST=0.0.0.0
API_PORT=8000
```

### Step 5: Create Basic FastAPI App
Create `backend/app/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

logger = structlog.get_logger()

app = FastAPI(
    title="CH Health OS API",
    description="Private health operating system",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "service": "CH Health OS API",
        "status": "healthy",
        "version": "0.1.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Step 6: Test Local Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Mac/Linux)
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn app.main:app --reload

# Test: Open http://localhost:8000
# Test: Open http://localhost:8000/docs (FastAPI auto-docs)
```

---

## Phase 1B: Supabase Setup (Day 1-2)

### Step 1: Create Supabase Project (if not exists)
1. Go to supabase.com
2. Create new project: "ch-health-os"
3. Region: Choose closest to Austin (e.g., US West)
4. Database password: Generate strong password (save it)
5. Wait for project to provision (~2 minutes)

### Step 2: Get Supabase Credentials
1. Go to Project Settings > API
2. Copy:
   - Project URL
   - `anon` `public` key
   - `service_role` `secret` key
3. Add to `backend/.env`

### Step 3: Connect via MCP (for you)
- Share Supabase project access via MCP
- We'll use MCP tools to run migrations

### Step 4: Run Initial Migrations
We'll create migration files based on `DATABASE_SCHEMA.md` and apply them.

---

## Phase 1C: Telegram Bot Setup (Day 2)

### Step 1: Create Telegram Bot
1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Choose name: "CH Health Vita"
5. Choose username: "ch_health_vita_bot" (or similar)
6. Copy the token (looks like `123456789:ABCdefGhIJKlmNOPQrsTUVwxyZ`)
7. Add to `backend/.env`

### Step 2: Configure Bot
```bash
# Set bot description
curl -X POST https://api.telegram.org/bot<YOUR_TOKEN>/setMyDescription \
  -H "Content-Type: application/json" \
  -d '{"description": "Vita - Your personal health assistant"}'

# Set bot commands
curl -X POST https://api.telegram.org/bot<YOUR_TOKEN>/setMyCommands \
  -H "Content-Type: application/json" \
  -d '{
    "commands": [
      {"command": "today", "description": "Ver rutinas de hoy"},
      {"command": "done", "description": "Marcar como completo"},
      {"command": "status", "description": "Ver progreso"},
      {"command": "help", "description": "Ayuda"}
    ]
  }'
```

### Step 3: Test Bot
1. Search for your bot in Telegram
2. Send `/start`
3. Bot should respond (we'll implement this)

---

## Phase 1D: Database Migrations (Day 2-3)

We'll create SQL migration files from the schema and apply them.

**Migration files to create:**
1. `001_initial_schema.sql` — Core tables
2. `002_routines.sql` — Routine system
3. `003_habits_exercise.sql` — Habits + exercise
4. (etc.)

**Apply via:**
- Supabase dashboard SQL editor, or
- Supabase CLI, or
- MCP Supabase tools

---

## Phase 1E: Deploy to Render (Day 3)

### Step 1: Create Render Account
1. Go to render.com
2. Sign up with GitHub

### Step 2: Create Web Service
1. Dashboard > New > Web Service
2. Connect your GitHub repo
3. Configure:
   - Name: `ch-health-api`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Instance Type: Free (for now)

### Step 3: Add Environment Variables
Add all variables from `.env.example` in Render dashboard

### Step 4: Deploy
- Push to GitHub → Auto-deploy
- Get your URL: `https://ch-health-api.onrender.com`

### Step 5: Set Telegram Webhook
```bash
curl -X POST https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook \
  -H "Content-Type: application/json" \
  -d '{"url": "https://ch-health-api.onrender.com/api/telegram/webhook"}'
```

---

## Phase 2 Preview: Core Features (Week 1-2)

Once foundation is set, we'll build:
1. **Database service layer** — RoutineService, HabitService
2. **REST API endpoints** — CRUD for routines, habits
3. **Scoring engine** — Daily score calculation
4. **Telegram webhook handler** — Receive messages
5. **Basic Vita agent** — Respond to commands

---

## Prerequisites Confirmed ✅

1. ✅ **Render account** — Ready
2. ✅ **GitHub repository** — Initialized
3. ✅ **OpenAI API key** — Available
4. ✅ **ORM choice** — SQLAlchemy (type safety, beginner-friendly)
5. ✅ **Timeline** — Full MVP with dashboard (6-8 weeks)
6. ⏳ **Supabase project** — Will be shared
7. ⏳ **Telegram bot token** — Will be shared

See `PROJECT_CONVENTIONS.md` for detailed coding standards and best practices.

---

## My Recommendations for Next Actions

### Immediate (Today/Tomorrow):
1. ✅ Review MASTER_PLAN.md (done)
2. ✅ Review DATABASE_SCHEMA.md (done)
3. Initialize Git repository
4. Set up backend project structure
5. Create Telegram bot
6. Test local FastAPI app

### This Week:
1. Create Supabase project
2. Share Supabase MCP access
3. Create and run database migrations
4. Deploy basic API to Render
5. Connect Telegram webhook

### Next Week:
1. Implement RoutineService
2. Build REST API endpoints
3. Implement scoring logic
4. Add Telegram command handlers

---

## Questions for You

1. **Do you have a Render account?**
2. **Do you have a GitHub repo?** (public or private?)
3. **Do you have an OpenAI API key?** (for LangGraph/Vita)
4. **Is Supabase project already created?**
5. **Python experience level?** (this helps me calibrate explanations)
6. **Preferred timeline?** Aggressive (Telegram-only) or Moderate (full dashboard)?

---

## Ready to Start?

I can help you with:
- Creating the Git repository structure
- Setting up the backend skeleton
- Writing the database migrations
- Creating the Telegram bot
- Deploying to Render

**What would you like to tackle first?**
