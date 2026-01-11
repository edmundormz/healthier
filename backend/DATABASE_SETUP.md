# Database Setup Guide

**Date:** January 10, 2026  
**Status:** Step-by-step instructions for database configuration

---

## Overview

This guide walks you through setting up the Supabase Postgres database connection for CH Health OS.

**What you'll do:**
1. Get your database password from Supabase
2. Get your Postgres connection string
3. Get your service_role API key
4. Create your `.env` file
5. Apply database migrations
6. Test the connection

---

## Step 1: Get Your Supabase API Keys

Supabase uses a new key system with **publishable** and **secret** keys.

1. Go to: https://supabase.com/dashboard/project/ekttjvqjkvvpavewsxhb/settings/api
2. Under "API Keys" section, you'll find:
   - **Publishable key** (starts with `sb_publishable_...`) - Already in your `.env`
   - **Secret key** (starts with `sb_secret_...`) - This is what you need

3. Click to reveal and copy the **secret** key
4. It will start with `sb_secret_...`

⚠️ **Warning**: The secret key has elevated privileges. Never expose it in frontend code or commit it to git!

**Note:** The old `anon` and `service_role` keys are deprecated. We're using the new system.

---

## Step 2: Update Your .env File

1. Open `backend/.env` in your editor
2. Find the line: `SUPABASE_SECRET_KEY=your_secret_key_here`
3. Replace `your_secret_key_here` with the secret key you copied from Step 1

```bash
# Should look like this:
SUPABASE_SECRET_KEY=sb_secret_gDna-iKOKz2RvAbqzPN35A_QSFSz9FM
```

4. Save the file

**The other values are already filled in:**
- ✅ `SUPABASE_URL` - Already set
- ✅ `SUPABASE_PUBLISHABLE_KEY` - Already set
- ✅ `TELEGRAM_BOT_TOKEN` - Already set

**Optional (for later):**
- `OPENAI_API_KEY` - Add when building Vita AI agent

---

## Step 3: Apply Database Migrations

Once your `.env` file is configured, apply the database schema:

### Using Supabase MCP (Recommended)

The database migrations will be applied automatically via the Supabase MCP connection.

### Manual SQL (Alternative)

If needed, you can also apply migrations manually:

1. Go to: https://supabase.com/dashboard/project/ekttjvqjkvvpavewsxhb/editor
2. Open the SQL Editor
3. Copy and paste migration files from `backend/migrations/`
4. Execute each migration in order

---

## Step 4: Test the Connection

### Test 1: Start the Backend Server

```bash
cd backend
poetry shell
poetry run uvicorn app.main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**If you see errors:**
- Check that your `.env` file exists
- Verify the connection string format
- Confirm your password is correct
- Ensure no extra spaces in the `.env` values

### Test 2: Check Health Endpoint

Open your browser or use curl:

```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "environment": "development",
  "database": "connected"
}
```

### Test 3: Check API Docs

Open: http://localhost:8000/docs

You should see the FastAPI interactive documentation.

---

## Common Issues & Solutions

### Issue: "Connection refused" or "Could not connect to server"

**Cause**: Secret key is incorrect or connection issue.

**Solution**:
1. Verify your secret key is correct (starts with `sb_secret_`)
2. Check for extra spaces in `.env`
3. Ensure the key is properly copied from Supabase dashboard
4. Restart the server

### Issue: "Authentication failed"

**Cause**: Secret key is incorrect or expired.

**Solution**:
1. Go back to Supabase dashboard -> Settings -> API
2. Copy the secret key again (NOT the publishable key)
3. Update `.env` file with `SUPABASE_SECRET_KEY=sb_secret_...`
4. Restart the server

### Issue: "Module not found" or import errors

**Cause**: Dependencies not installed.

**Solution**:
```bash
cd backend
poetry install
poetry shell
```

---

## Security Checklist

Before deploying to production:

- [ ] `.env` file is in `.gitignore` ✅ (already configured)
- [ ] Never commit `.env` to git
- [ ] Secret key only used in backend (never in frontend)
- [ ] Publishable key is safe for frontend use
- [ ] Production `SECRET_KEY` is random (use: `openssl rand -hex 32`)
- [ ] `DEBUG=false` in production
- [ ] `CORS_ORIGINS` updated to actual frontend URL

---

## Quick Reference

### Your Project Details

- **Project Name**: healthier
- **Project ID**: ekttjvqjkvvpavewsxhb
- **API URL**: https://ekttjvqjkvvpavewsxhb.supabase.co
- **Dashboard**: https://supabase.com/dashboard/project/ekttjvqjkvvpavewsxhb

### Key Files

- `.env` - Your environment variables (create from `.env.example`)
- `.env.example` - Template with all required variables
- `app/core/config.py` - Configuration loading logic
- `app/core/database.py` - Database connection setup
- `migrations/` - SQL migration files

### Useful Commands

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Start development server
poetry run uvicorn app.main:app --reload

# Run tests
poetry run pytest

# Format code
poetry run black app/

# Lint code
poetry run ruff check app/
```

---

## Next Steps

Once your database is connected:

1. ✅ Verify all tables are created
2. ✅ Create SQLAlchemy models
3. ✅ Test CRUD operations
4. ✅ Set up Row Level Security (RLS) policies
5. ✅ Create seed data for testing
6. ✅ Build API endpoints

---

**Last Updated:** January 10, 2026
