# Database Connection Guide

**Date:** January 10, 2026, 9:10 PM CST

---

## 🔐 Connection Information

### Transaction Pooler (Primary - For Application)

```bash
# PostgreSQL CLI command
psql -h aws-0-us-west-2.pooler.supabase.com -p 6543 -d postgres -U postgres.ekttjvqjkvvpavewsxhb

# SQLAlchemy Connection String
DATABASE_URL=postgresql+asyncpg://postgres.ekttjvqjkvvpavewsxhb:q8%23bdm.ZL%40Di%2CRq@aws-0-us-west-2.pooler.supabase.com:6543/postgres
```

### Direct Connection (For Migrations)

```bash
# PostgreSQL CLI command  
psql -h aws-0-us-west-2.pooler.supabase.com -p 5432 -d postgres -U postgres.ekttjvqjkvvpavewsxhb

# SQLAlchemy Connection String
DIRECT_URL=postgresql+asyncpg://postgres.ekttjvqjkvvpavewsxhb:q8%23bdm.ZL%40Di%2CRq@aws-0-us-west-2.pooler.supabase.com:5432/postgres
```

---

## 🔑 Password URL Encoding

**Original Password:** `q8#bdm.ZL@Di,Rq`

**URL-Encoded Password:** `q8%23bdm.ZL%40Di%2CRq`

### Why URL Encode?

Your password contains special characters that have meaning in URLs:
- `#` → `%23` (hash/fragment identifier)
- `@` → `%40` (credentials separator)
- `,` → `%2C` (comma)

If you don't encode them, the connection string parser will misinterpret them and fail to connect.

---

## 📝 Your `.env` File

Copy this exact configuration to `backend/.env`:

```bash
# =============================================================================
# DATABASE CONFIGURATION (SQLAlchemy)
# =============================================================================
DATABASE_URL=postgresql+asyncpg://postgres.ekttjvqjkvvpavewsxhb:q8%23bdm.ZL%40Di%2CRq@aws-0-us-west-2.pooler.supabase.com:6543/postgres
DIRECT_URL=postgresql+asyncpg://postgres.ekttjvqjkvvpavewsxhb:q8%23bdm.ZL%40Di%2CRq@aws-0-us-west-2.pooler.supabase.com:5432/postgres

# =============================================================================
# SUPABASE CONFIGURATION
# =============================================================================
SUPABASE_URL=https://ekttjvqjkvvpavewsxhb.supabase.co
SUPABASE_PUBLISHABLE_KEY=sb_publishable_i4s7XifpKe1WVj9nAi55wg_KQ60frnZ
SUPABASE_SECRET_KEY=your_secret_key_here

# =============================================================================
# TELEGRAM BOT
# =============================================================================
TELEGRAM_BOT_TOKEN=8533710273:AAEKPctRqKNTkpuu3pJY7mawLxhT3SqE2V8
TELEGRAM_WEBHOOK_SECRET=ch_health_vita_webhook_secret_2026

# =============================================================================
# OPENAI
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
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# =============================================================================
# LOGGING
# =============================================================================
LOG_LEVEL=INFO
```

---

## 🚀 Start the Server

```bash
cd backend
poetry shell
poetry run uvicorn app.main:app --reload
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories: ['C:\\Users\\HectorRamirez\\Desktop\\Sandbox\\healthier\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXX] using WatchFiles
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     application_startup - environment: development, debug: True, database: SQLAlchemy + asyncpg + Supabase Postgres
INFO:     database_initialized - note: Using existing Supabase schema
INFO:     database_connected - status: success, orm: SQLAlchemy 2.0
INFO:     Application startup complete.
```

---

## 🧪 Test the Connection

### 1. Root Endpoint
```bash
curl http://localhost:8000/
```

Expected:
```json
{
  "service": "CH Health OS API",
  "status": "healthy",
  "version": "0.1.0",
  "docs": "/docs"
}
```

### 2. Health Check
```bash
curl http://localhost:8000/health
```

Expected:
```json
{
  "status": "ok",
  "environment": "development",
  "database": "connected"
}
```

### 3. Test SQLAlchemy ORM
```bash
curl http://localhost:8000/api/test/users
```

Expected:
```json
{
  "status": "success",
  "orm": "SQLAlchemy 2.0",
  "count": 0,
  "users": []
}
```

### 4. API Documentation
Open in browser: http://localhost:8000/docs

You should see the FastAPI interactive documentation.

---

## 🔍 Connection Details

### Transaction Pooler (Port 6543)
- **Use for:** Application runtime (FastAPI app)
- **Mode:** Transaction pooling via pgbouncer
- **Benefits:** 
  - Efficient connection reuse
  - Handles many concurrent requests
  - Automatic connection recycling
- **Limitations:**
  - Some PostgreSQL features not available (e.g., LISTEN/NOTIFY)
  - No long-running transactions

### Direct Connection (Port 5432)
- **Use for:** Database migrations (Alembic)
- **Mode:** Direct to Postgres
- **Benefits:**
  - Full PostgreSQL feature support
  - Can run DDL operations (CREATE TABLE, ALTER TABLE)
  - No limitations on transaction length
- **When to use:**
  - Running Alembic migrations
  - Long-running analytical queries
  - Admin operations

---

## 🐛 Troubleshooting

### "Connection refused" or "Invalid password"

**Check 1:** Verify URL encoding
```bash
# ❌ Wrong (raw password)
DATABASE_URL=postgresql+asyncpg://postgres.ekttjvqjkvvpavewsxhb:q8#bdm.ZL@Di,Rq@...

# ✅ Correct (URL-encoded password)
DATABASE_URL=postgresql+asyncpg://postgres.ekttjvqjkvvpavewsxhb:q8%23bdm.ZL%40Di%2CRq@...
```

**Check 2:** Verify .env file location
- File should be: `backend/.env`
- NOT: `healthier/.env` (wrong location)

**Check 3:** No extra spaces
```bash
# ❌ Wrong (space before =)
DATABASE_URL =postgresql+asyncpg://...

# ✅ Correct (no spaces)
DATABASE_URL=postgresql+asyncpg://...
```

### "ValidationError: Field required"

This means Pydantic can't find DATABASE_URL or DIRECT_URL in your `.env` file.

**Solution:** Add both lines to `backend/.env`

### "Module not found"

```bash
cd backend
poetry install
poetry shell
```

---

## 📊 Connection String Format

```
postgresql+asyncpg://USERNAME:PASSWORD@HOST:PORT/DATABASE
                   └─────────┬────────┘ └──┬──┘ └┬┘ └──┬──┘
                          User Info     Host  Port  Database
```

### Your Configuration:
- **Driver:** `postgresql+asyncpg` (async Postgres via asyncpg)
- **Username:** `postgres.ekttjvqjkvvpavewsxhb`
- **Password:** `q8%23bdm.ZL%40Di%2CRq` (URL-encoded)
- **Host:** `aws-0-us-west-2.pooler.supabase.com`
- **Port:** `6543` (pooler) or `5432` (direct)
- **Database:** `postgres`

---

## ✅ Verification Checklist

Before starting the server:

- [ ] `.env` file exists in `backend/` directory
- [ ] `DATABASE_URL` is set with URL-encoded password
- [ ] `DIRECT_URL` is set with URL-encoded password
- [ ] Password is encoded: `q8%23bdm.ZL%40Di%2CRq`
- [ ] Port 6543 for pooler (DATABASE_URL)
- [ ] Port 5432 for direct (DIRECT_URL)
- [ ] No spaces around `=` signs
- [ ] File has no BOM or special characters

---

## 🎉 Success!

Once the server starts successfully, you have:

✅ **Direct Postgres connection** via asyncpg  
✅ **Transaction pooling** for efficient connections  
✅ **SQLAlchemy ORM** with full type safety  
✅ **Production-ready architecture**  

---

**Last Updated:** January 10, 2026, 9:10 PM CST
