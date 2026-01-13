# Render Environment Variables - Production

**Date:** January 12, 2026, 8:00 PM CST  
**Purpose:** Environment variables for Render deployment  
**Custom Domains:**
- Backend: `healthier-api.inventasolutions.ai`
- Frontend: `healthier.inventasolutions.ai`

---

## 📋 How to Add These to Render

1. Go to Render Dashboard → Your Service
2. Click **Environment** tab
3. Add each variable below (click "Add Environment Variable")
4. Deploy after adding all variables

---

## 🔑 Required Environment Variables

Copy these **exactly as shown**, replacing only the values marked with `REPLACE_WITH_YOUR_XXX`:

### Supabase Configuration

```
SUPABASE_URL
https://ekttjvqjkvvpavewsxhb.supabase.co
```

```
SUPABASE_PUBLISHABLE_KEY
sb_publishable_i4s7XifpKe1WVj9nAi55wg_KQ60frnZ
```

```
SUPABASE_SECRET_KEY
REPLACE_WITH_YOUR_SUPABASE_SECRET_KEY
```

**Where to get:** [Supabase Dashboard → API Settings](https://supabase.com/dashboard/project/ekttjvqjkvvpavewsxhb/settings/api)

---

### Database Configuration

```
DATABASE_URL
postgresql+asyncpg://postgres.ekttjvqjkvvpavewsxhb:REPLACE_WITH_YOUR_DB_PASSWORD@aws-0-us-west-2.pooler.supabase.com:6543/postgres?pgbouncer=true
```

```
DIRECT_URL
postgresql+asyncpg://postgres.ekttjvqjkvvpavewsxhb:REPLACE_WITH_YOUR_DB_PASSWORD@aws-0-us-west-2.pooler.supabase.com:5432/postgres
```

**Where to get password:** Supabase Dashboard → Settings → Database → Database Password

---

### Telegram Bot

```
TELEGRAM_BOT_TOKEN
8533710273:AAEKPctRqKNTkpuu3pJY7mawLxhT3SqE2V8
```

```
TELEGRAM_WEBHOOK_SECRET
ch_health_vita_webhook_secret_2026
```

---

### OpenAI (for Vita Agent)

```
OPENAI_API_KEY
REPLACE_WITH_YOUR_OPENAI_API_KEY
```

**Where to get:** [OpenAI Platform → API Keys](https://platform.openai.com/api-keys)  
**Note:** Only needed when you implement the Vita LangGraph agent

---

### Application Settings

```
ENVIRONMENT
production
```

```
DEBUG
false
```

```
TIMEZONE
America/Chicago
```

---

### API Configuration

```
API_HOST
0.0.0.0
```

```
API_PORT
${PORT}
```
**Note:** `${PORT}` uses Render's automatic port - don't change this!

```
API_TITLE
CH Health OS API
```

```
API_VERSION
0.1.0
```

---

### CORS Settings

```
CORS_ORIGINS
https://healthier.inventasolutions.ai,http://localhost:3000
```

**IMPORTANT:** 
- No spaces after commas!
- Update when frontend URL changes
- Add more origins if needed (separate with commas)

---

### Logging

```
LOG_LEVEL
INFO
```

---

## 🚀 Deployment Configuration

**Service Settings:**
- **Name:** `ch-health-api`
- **Runtime:** Python 3
- **Root Directory:** `backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## 🌐 Custom Domain Setup

**After initial deployment succeeds:**

1. Go to Render Dashboard → Your Service → **Settings** tab
2. Scroll to **Custom Domains** section
3. Click **Add Custom Domain**
4. Enter: `healthier-api.inventasolutions.ai`
5. Render will provide a **CNAME record**, something like:
   ```
   healthier-api.inventasolutions.ai → your-service.onrender.com
   ```
6. Add this CNAME record in your DNS provider (InventaSolutions DNS)
7. Wait for DNS propagation (usually 15-30 minutes)
8. Render will automatically provision SSL certificate

---

## ✅ Checklist

Before deploying:

- [ ] Copied all environment variables to Render
- [ ] Replaced `REPLACE_WITH_YOUR_DB_PASSWORD` with actual password
- [ ] Replaced `REPLACE_WITH_YOUR_SUPABASE_SECRET_KEY` with actual key
- [ ] Verified `CORS_ORIGINS` includes your frontend domain
- [ ] Confirmed build and start commands
- [ ] Set root directory to `backend`

After initial deploy:

- [ ] Test health endpoint: `https://your-service.onrender.com/health`
- [ ] Test API docs: `https://your-service.onrender.com/docs`
- [ ] Add custom domain `healthier-api.inventasolutions.ai`
- [ ] Update DNS records
- [ ] Wait for SSL certificate
- [ ] Test custom domain: `https://healthier-api.inventasolutions.ai/health`

---

## 🔗 Update Frontend

After backend is deployed, update Vercel:

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Update or add:
   ```
   NEXT_PUBLIC_API_URL
   https://healthier-api.inventasolutions.ai
   ```
3. Redeploy frontend

---

## 🐛 Troubleshooting

### Build Fails
- Check Python version (needs 3.11+)
- Check build logs for missing dependencies
- Verify `requirements.txt` is in `backend/` directory

### App Crashes on Start
- Check environment variables are set correctly
- Check database password is correct
- Check Render logs: Dashboard → Logs tab

### Database Connection Error
- Verify `DATABASE_URL` and `DIRECT_URL` are correct
- Verify Supabase database is running
- Check if Supabase password has special characters (may need URL encoding)

### CORS Errors
- Verify `CORS_ORIGINS` includes your frontend URL
- Check for spaces in CORS_ORIGINS (should be none!)
- Frontend URL must match exactly (including https://)

### 502 Bad Gateway
- Check if app is listening on `$PORT` (not hardcoded port)
- Verify start command uses `--port $PORT`

---

**Last Updated:** January 12, 2026, 8:00 PM CST
