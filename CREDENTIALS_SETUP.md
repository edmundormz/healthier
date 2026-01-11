# Credentials Setup Guide

**Date:** January 10, 2026, 2:06 PM CST  
**Status:** Partial — Telegram bot ready, Supabase pending

---

## ✅ Credentials Received

### Telegram Bot
- **Bot Name:** Vita
- **Token:** ✅ Received and configured
- **Status:** Ready to use

### Supabase Project
- **Project Name:** healthier
- **Status:** ⏳ Need API credentials

---

## 📋 Next Steps

### 1. Get Supabase Credentials

**Where to find them:**
1. Go to [supabase.com](https://supabase.com)
2. Open your "healthier" project
3. Go to: **Settings** > **API**

**Copy these values:**
- **Project URL** (looks like: `https://xxxxx.supabase.co`) - ✅ Already in `.env`
- **Publishable key** (starts with `sb_publishable_...`) - ✅ Already in `.env`
- **Secret key** (starts with `sb_secret_...`) - ⚠️ You need to add this

**⚠️ Important:**
- The `secret` key has elevated privileges for backend operations
- NEVER expose it in frontend code
- NEVER commit it to git
- Only use it in backend (Render environment variables)
- The `publishable` key is safe to use in frontend

**Note:** The old `anon` and `service_role` keys are deprecated. Supabase now uses publishable/secret keys.

---

## 🔧 Setting Up Your `.env` File

### For Local Development

Create `backend/.env` file manually with:

```bash
# Supabase Configuration (New Key System)
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

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Security
SECRET_KEY=ch_health_dev_secret_key_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Logging
LOG_LEVEL=INFO
```

**Replace these values:**
- `SUPABASE_SECRET_KEY` — Your secret key (get from dashboard)
- `OPENAI_API_KEY` — Your OpenAI API key (for later)

---

## 🚀 For Render Deployment

When deploying to Render, add these as **Environment Variables**:

1. Go to Render dashboard
2. Select your web service
3. Go to **Environment** tab
4. Add each variable from your `.env` file

**⚠️ Change for production:**
- `ENVIRONMENT=production`
- `DEBUG=false`
- Generate strong `SECRET_KEY` (use: `openssl rand -hex 32`)
- Update `CORS_ORIGINS` to your actual frontend URL

---

## 🔐 Security Checklist

- [ ] `.env` file is in `.gitignore` ✅ (already configured)
- [ ] Never commit `.env` to git
- [ ] Secret key only used in backend (never in frontend)
- [ ] Publishable key is safe for frontend use
- [ ] Production `SECRET_KEY` is random and secure
- [ ] Webhook secret is random and secure
- [ ] OpenAI API key has usage limits set

---

## 📝 Credentials Status

| Credential | Status | Location |
|------------|--------|----------|
| Telegram Bot Token | ✅ Configured | `backend/.env` |
| Supabase URL | ✅ Configured | `backend/.env` |
| Supabase Publishable Key | ✅ Configured | `backend/.env` |
| Supabase Secret Key | ⏳ Pending | Need from dashboard |
| OpenAI API Key | ⏳ Pending | User to provide |

---

## 🧪 Testing Telegram Bot

Once credentials are set up, test the bot:

```bash
# Test bot info
curl https://api.telegram.org/bot8533710273:AAEKPctRqKNTkpuu3pJY7mawLxhT3SqE2V8/getMe
```

**Expected response:**
```json
{
  "ok": true,
  "result": {
    "id": 8533710273,
    "is_bot": true,
    "first_name": "Vita",
    "username": "your_bot_username"
  }
}
```

---

## 🔗 Useful Links

- [Supabase Dashboard](https://supabase.com/dashboard)
- [Telegram Bot API Docs](https://core.telegram.org/bots/api)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [Render Dashboard](https://dashboard.render.com)

---

**Last Updated:** January 10, 2026, 2:06 PM CST
