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
# Get from: https://supabase.com/dashboard/project/ekttjvqjkvvpavewsxhb/settings/api

# Project URL (already filled in)
SUPABASE_URL=https://ekttjvqjkvvpavewsxhb.supabase.co

# Publishable key (safe for frontend, already filled in)
SUPABASE_PUBLISHABLE_KEY=sb_publishable_i4s7XifpKe1WVj9nAi55wg_KQ60frnZ

# Secret key (SECRET - backend only)
# ⚠️ TODO: Get from dashboard -> Settings -> API -> "secret" key
SUPABASE_SECRET_KEY=your_secret_key_here

# Telegram Bot - Vita
TELEGRAM_BOT_TOKEN=8533710273:AAEKPctRqKNTkpuu3pJY7mawLxhT3SqE2V8
TELEGRAM_WEBHOOK_SECRET=ch_health_vita_webhook_secret_2026

# OpenAI (for LangGraph/Vita)
OPENAI_API_KEY=your_openai_api_key_here

# Application Settings
ENVIRONMENT=development
DEBUG=true
TIMEZONE=America/Chicago

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_TITLE=CH Health OS API
API_VERSION=0.1.0

# CORS (comma-separated origins)
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Security
SECRET_KEY=ch_health_dev_secret_key_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Logging
LOG_LEVEL=INFO
```

## Keys Already Filled In

✅ **SUPABASE_URL** - Already set to your project  
✅ **SUPABASE_PUBLISHABLE_KEY** - Already set (new publishable key)  
✅ **TELEGRAM_BOT_TOKEN** - Already set (Vita bot verified)

## Keys You Need to Add

⏳ **SUPABASE_SECRET_KEY** - Get from Supabase dashboard  
⏳ **OPENAI_API_KEY** - Get from OpenAI platform (for Vita agent)

## About Supabase Keys

Supabase uses a new key system:

- **Publishable key** (`sb_publishable_...`) - Safe for frontend/client-side
- **Secret key** (`sb_secret_...`) - Backend only, provides elevated privileges

The old `anon` and `service_role` keys are deprecated. This project uses the new system.
