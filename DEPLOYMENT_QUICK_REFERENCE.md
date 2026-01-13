# Deployment Quick Reference

**Date:** January 12, 2026, 8:30 PM CST

---

## 🚀 Backend Deployment (Render)

### Configuration

| Setting | Value |
|---------|-------|
| **Service Name** | `ch-health-api` |
| **Runtime** | Python 3 |
| **Root Directory** | `backend` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

### Environment Variables

See: `backend/.env.backend` or `backend/RENDER_ENV_VARIABLES.md`

**Required:**
- `SUPABASE_URL`
- `SUPABASE_PUBLISHABLE_KEY`
- `SUPABASE_SECRET_KEY`
- `DATABASE_URL`
- `DIRECT_URL`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_WEBHOOK_SECRET`
- `OPENAI_API_KEY`
- `ENVIRONMENT=production`
- `DEBUG=false`
- `TIMEZONE=America/Chicago`
- `API_HOST=0.0.0.0`
- `API_PORT=${PORT}`
- `API_TITLE=healthier-api-inventa`
- `API_VERSION=0.1.0`
- `CORS_ORIGINS=https://healthier.inventasolutions.ai,http://localhost:3000`
- `LOG_LEVEL=INFO`

### Custom Domain

**Domain:** `healthier-api.inventasolutions.ai`

1. Deploy first with Render's default URL
2. Add custom domain in Render Settings
3. Add CNAME record in DNS:
   ```
   Type: CNAME
   Name: healthier-api
   Value: your-service.onrender.com
   ```

---

## 🌐 Frontend Deployment (Vercel)

### Configuration

| Setting | Value |
|---------|-------|
| **Framework** | Next.js (auto-detected) |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` (default) |
| **Output Directory** | `.next` (default) |
| **Install Command** | `npm install` (default) |
| **Node Version** | 18.x+ (automatic) |

### Environment Variables

See: `frontend/.env.frontend` or `frontend/VERCEL_DEPLOYMENT.md`

**Required (only 3):**
- `NEXT_PUBLIC_SUPABASE_URL=https://ekttjvqjkvvpavewsxhb.supabase.co`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_i4s7XifpKe1WVj9nAi55wg_KQ60frnZ`
- `NEXT_PUBLIC_API_URL=https://healthier-api.inventasolutions.ai`

### Custom Domain

**Domain:** `healthier.inventasolutions.ai`

1. Deploy first with Vercel's default URL
2. Add custom domain in Vercel Settings → Domains
3. Add CNAME record in DNS:
   ```
   Type: CNAME
   Name: healthier
   Value: cname.vercel-dns.com
   ```

---

## 📋 Deployment Order

1. ✅ **Deploy Backend First** (Render)
   - Get backend URL
   - Test health endpoint: `https://healthier-api.onrender.com/health`
   - Note down the URL for frontend

2. ✅ **Deploy Frontend** (Vercel)
   - Use backend URL in `NEXT_PUBLIC_API_URL`
   - Test preview URL
   - Verify API connectivity

3. ✅ **Add Custom Domains** (Both)
   - Add domains in Render and Vercel
   - Configure DNS records
   - Wait for SSL certificates

4. ✅ **Test Production**
   - Visit `https://healthier.inventasolutions.ai`
   - Test signup/login
   - Test CRUD operations

---

## 🔍 Health Check URLs

**Backend:**
- Default: `https://your-service.onrender.com/health`
- Custom: `https://healthier-api.inventasolutions.ai/health`
- API Docs: `https://healthier-api.inventasolutions.ai/docs`

**Frontend:**
- Default: `https://your-project.vercel.app`
- Custom: `https://healthier.inventasolutions.ai`

---

## 🐛 Quick Troubleshooting

### Backend Won't Start
- Check Render logs for errors
- Verify `DATABASE_URL` is correct
- Check Python version (needs 3.11+)

### Frontend Build Fails
- Verify `Root Directory` is set to `frontend`
- Check environment variables are set
- Run `npm run build` locally first

### CORS Errors
- Verify backend `CORS_ORIGINS` includes frontend URL
- Check `NEXT_PUBLIC_API_URL` matches backend URL
- Ensure no trailing slashes

### Auth Not Working
- Verify Supabase keys in both backend and frontend
- Check Supabase project is active
- Test locally first

---

## 📚 Full Documentation

- **Backend:** `backend/RENDER_ENV_VARIABLES.md`
- **Frontend:** `frontend/VERCEL_DEPLOYMENT.md`
- **Testing:** `TESTING_AND_DEPLOYMENT_PLAN.md`

---

**Last Updated:** January 12, 2026, 8:30 PM CST
