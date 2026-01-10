# Environment Variables Reference

Your `.env` file should contain these values:

```bash
# Supabase Configuration (New Key System)
# Get these from: https://supabase.com/dashboard > Project Settings > API
SUPABASE_URL=https://ekttjvqjkvvpavewsxhb.supabase.co
SUPABASE_PUBLISHABLE_KEY=sb_publishable_i4s7XifpKe1WVj9nAi55wg_KQ60frnZ
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

⏳ **SUPABASE_SECRET_KEY** - Get from Supabase dashboard (replaces service_role key)
⏳ **OPENAI_API_KEY** - Get from OpenAI platform (for Vita agent)

## Note on Supabase Keys

Supabase is transitioning from the old key system to a new one:

**Old System (Legacy):**
- `anon` key (public, safe for frontend)
- `service_role` key (secret, backend only)

**New System (Current):**
- `publishable` key (replaces anon, starts with `sb_publishable_`)
- `secret` key (replaces service_role, backend only)

We're using the new system for this project.
