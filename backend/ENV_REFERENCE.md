# Environment Variables Reference

⚠️ **IMPORTANT**: Your `.env` file should contain these values.

## Supabase New Key System

Supabase now uses **publishable** and **secret** keys (the old anon/service_role keys are deprecated).

### How to Get Your Keys

1. Go to: https://supabase.com/dashboard/project/ekttjvqjkvvpavewsxhb/settings/api
2. Under "API Keys" section, you'll find:
   - **Publishable key** (starts with `sb_publishable_`) - Safe for frontend
   - **Secret key** (starts with `sb_secret_`) - Backend only, NEVER expose

---

## Complete .env File Template

```bash
# =============================================================================
# SUPABASE CONFIGURATION
# =============================================================================
SUPABASE_URL=https://ekttjvqjkvvpavewsxhb.supabase.co
SUPABASE_PUBLISHABLE_KEY=sb_publishable_i4s7XifpKe1WVj9nAi55wg_KQ60frnZ
SUPABASE_SECRET_KEY=your_secret_key_here

# =============================================================================
# DATABASE CONFIGURATION (SQLAlchemy)
# =============================================================================
# Connection pooling (use for application runtime - pgbouncer transaction mode)
DATABASE_URL=postgresql+asyncpg://postgres.ekttjvqjkvvpavewsxhb:YOUR_PASSWORD@aws-0-us-west-2.pooler.supabase.com:6543/postgres?pgbouncer=true

# Direct connection (use for migrations - bypasses pgbouncer)
DIRECT_URL=postgresql+asyncpg://postgres.ekttjvqjkvvpavewsxhb:YOUR_PASSWORD@aws-0-us-west-2.pooler.supabase.com:5432/postgres

# =============================================================================
# TELEGRAM BOT - VITA
# =============================================================================
TELEGRAM_BOT_TOKEN=8533710273:AAEKPctRqKNTkpuu3pJY7mawLxhT3SqE2V8
TELEGRAM_WEBHOOK_SECRET=ch_health_vita_webhook_secret_2026

# =============================================================================
# OPENAI (for LangGraph/Vita)
# =============================================================================
OPENAI_API_KEY=your_openai_api_key_here

# =============================================================================
# APPLICATION SETTINGS
# =============================================================================
ENVIRONMENT=development
DEBUG=true
TIMEZONE=America/Chicago

# =============================================================================
# API CONFIGURATION
# =============================================================================
API_HOST=0.0.0.0
API_PORT=8000
API_TITLE=CH Health OS API
API_VERSION=0.1.0

# =============================================================================
# CORS (comma-separated origins)
# =============================================================================
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# =============================================================================
# LOGGING
# =============================================================================
LOG_LEVEL=INFO
```

## Keys Already Filled In

✅ **SUPABASE_URL** - Already set to your project  
✅ **SUPABASE_PUBLISHABLE_KEY** - Already set (new publishable key)  
✅ **TELEGRAM_BOT_TOKEN** - Already set (Vita bot verified)

## Keys You Need to Add

⏳ **SUPABASE_SECRET_KEY** - Get from Supabase dashboard (optional, for Supabase Auth/Storage)
⚠️ **DATABASE_URL** - Replace YOUR_PASSWORD with your database password  
⚠️ **DIRECT_URL** - Replace YOUR_PASSWORD with your database password  
⏳ **OPENAI_API_KEY** - Get from OpenAI platform (for Vita agent)

**Note**: The backend now uses **direct Postgres connection** (DATABASE_URL) via SQLAlchemy, not the Supabase REST API. The SUPABASE_SECRET_KEY is only needed if you want to use Supabase Auth or Storage features.

## About Supabase Keys

Supabase uses a new key system:

- **Publishable key** (`sb_publishable_...`) - Safe for frontend/client-side
- **Secret key** (`sb_secret_...`) - Backend only, provides elevated privileges

The old `anon` and `service_role` keys are deprecated. This project uses the new system.
