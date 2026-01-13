# Vercel Deployment Guide - Frontend

**Date:** January 12, 2026, 8:30 PM CST  
**Purpose:** Complete guide for deploying frontend to Vercel  
**Custom Domains:**
- Backend: `healthier-api.inventasolutions.ai`
- Frontend: `healthier.inventasolutions.ai`

---

## 📋 Environment Variables for Vercel

Copy these **exactly as shown** to Vercel Dashboard → Settings → Environment Variables:

### Supabase Configuration (Public Keys)

```
NEXT_PUBLIC_SUPABASE_URL
https://ekttjvqjkvvpavewsxhb.supabase.co
```

```
NEXT_PUBLIC_SUPABASE_ANON_KEY
sb_publishable_i4s7XifpKe1WVj9nAi55wg_KQ60frnZ
```

**Note:** These are PUBLIC keys - safe to expose in browser/client-side code. They only allow authenticated operations.

---

### Backend API URL

```
NEXT_PUBLIC_API_URL
https://healthier-api.inventasolutions.ai
```

**Important:**
- Use your custom domain if configured
- Or use Render's default URL: `https://your-service.onrender.com`
- Must match exactly (including https://)
- Backend must have this domain in CORS_ORIGINS

---

## 🚀 Vercel Deployment Steps

### Step 1: Connect GitHub Repository

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Select the repository: `healthier`

### Step 2: Configure Project Settings

**Framework Preset:** Next.js (auto-detected)

**Root Directory:** `frontend`
- Click **"Edit"** next to Root Directory
- Type: `frontend`
- This tells Vercel where your Next.js app is located

**Build Settings:**
- **Build Command:** `npm run build` (default, don't change)
- **Output Directory:** `.next` (default, don't change)
- **Install Command:** `npm install` (default, don't change)
- **Development Command:** `npm run dev` (default, don't change)

**Node.js Version:** 18.x or higher (automatic)

### Step 3: Add Environment Variables

1. In the import project screen, expand **"Environment Variables"**
2. Add the three variables listed above:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `NEXT_PUBLIC_API_URL`
3. Set **Environment:** All (Production, Preview, and Development)

**Alternative:** Add them after deployment in Settings → Environment Variables

### Step 4: Deploy

1. Click **"Deploy"**
2. Wait for build to complete (~2-3 minutes)
3. ✅ You'll get a URL like: `https://healthier-xyz.vercel.app`

---

## 🌐 Custom Domain Setup

**After initial deployment succeeds:**

### Step 1: Add Domain in Vercel

1. Go to Project Settings → **Domains**
2. Click **"Add Domain"**
3. Enter: `healthier.inventasolutions.ai`
4. Click **"Add"**

### Step 2: Configure DNS

Vercel will show you DNS records to add. You'll need to add:

**Option A - CNAME (Recommended):**
```
Type: CNAME
Name: healthier
Value: cname.vercel-dns.com
```

**Option B - A Record:**
```
Type: A
Name: healthier
Value: 76.76.21.21
```

### Step 3: Wait for Propagation

1. Add the DNS records in your DNS provider (InventaSolutions DNS)
2. Wait for DNS propagation (usually 5-15 minutes, max 48 hours)
3. Vercel will automatically provision SSL certificate
4. ✅ Your site will be live at `https://healthier.inventasolutions.ai`

---

## ✅ Deployment Checklist

### Before Deployment

- [ ] Backend is deployed and working on Render
- [ ] Backend URL confirmed (healthier-api.inventasolutions.ai)
- [ ] Backend CORS includes frontend URL
- [ ] Environment variables ready to copy

### During Deployment

- [ ] GitHub repository connected
- [ ] Root directory set to `frontend`
- [ ] Environment variables added (all 3)
- [ ] Build command confirmed: `npm run build`
- [ ] First deployment succeeded

### After Initial Deployment

- [ ] Test Vercel preview URL works
- [ ] Test signup/login flow
- [ ] Test API connectivity to backend
- [ ] Add custom domain
- [ ] Update DNS records
- [ ] Wait for SSL certificate
- [ ] Test custom domain works

---

## 🧪 Testing Production Frontend

### Test Basic Functionality

1. **Visit Site:**
   - Go to `https://healthier.inventasolutions.ai`
   - ✅ Page loads without errors

2. **Test Signup:**
   - Click "Sign Up"
   - Create test account
   - ✅ Should redirect to dashboard

3. **Test Login:**
   - Logout
   - Login with test account
   - ✅ Should redirect to dashboard

4. **Test API Integration:**
   - Try to create a routine
   - Try to view routines
   - ✅ Should communicate with backend

5. **Test Protected Routes:**
   - Logout
   - Try to access `/dashboard` directly
   - ✅ Should redirect to login

---

## 🐛 Troubleshooting

### Build Fails

**Error: "Cannot find module"**
- Check `package.json` is in `frontend/` directory
- Verify root directory is set to `frontend` in Vercel

**Error: "TypeScript errors"**
- Run `npm run build` locally first
- Fix any TypeScript errors
- Push fixes and redeploy

### Runtime Errors

**Error: "NEXT_PUBLIC_SUPABASE_URL is undefined"**
- Check environment variables are set in Vercel
- Verify variable names are exactly `NEXT_PUBLIC_*`
- Redeploy after adding variables

**Error: "Failed to fetch" or CORS errors**
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check backend CORS_ORIGINS includes your frontend URL
- Verify backend is running

**Error: "Unauthorized" or Auth issues**
- Verify Supabase keys are correct
- Check Supabase project is active
- Test login locally first

### Page Not Loading

**White screen or 500 error**
- Check Vercel deployment logs: Project → Deployments → Latest → View Logs
- Check browser console for errors (F12)
- Check Function Logs in Vercel dashboard

**Custom domain not working**
- Verify DNS records are correct
- Wait longer for DNS propagation (can take up to 48 hours)
- Check Vercel domain status: Settings → Domains

---

## 🔄 Redeploying After Changes

Vercel automatically redeploys when you push to GitHub:

1. Make changes to your code
2. Commit and push to GitHub
3. Vercel automatically builds and deploys
4. Check deployment status in Vercel dashboard

**Manual Redeploy:**
1. Go to Vercel Dashboard → Project
2. Click **"Deployments"**
3. Click **"..."** on any deployment
4. Click **"Redeploy"**

---

## 📊 Build Settings Summary

| Setting | Value |
|---------|-------|
| Framework | Next.js |
| Root Directory | `frontend` |
| Build Command | `npm run build` |
| Output Directory | `.next` |
| Install Command | `npm install` |
| Node Version | 18.x+ |

---

## 🔗 Important Links

- [Vercel Dashboard](https://vercel.com/dashboard)
- [Vercel Docs - Next.js](https://vercel.com/docs/frameworks/nextjs)
- [Vercel Docs - Environment Variables](https://vercel.com/docs/projects/environment-variables)
- [Vercel Docs - Custom Domains](https://vercel.com/docs/projects/domains)

---

## 🎯 Success Criteria

**Deployment Successful When:**
- ✅ Build completes without errors
- ✅ Preview URL works
- ✅ Can signup/login
- ✅ Can access protected routes
- ✅ API calls to backend work
- ✅ Custom domain working (if configured)
- ✅ SSL certificate active

---

## 📝 Environment Variables Reference

**For local development** (`.env.local`):
```bash
NEXT_PUBLIC_SUPABASE_URL=https://ekttjvqjkvvpavewsxhb.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_i4s7XifpKe1WVj9nAi55wg_KQ60frnZ
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**For production** (Vercel):
```bash
NEXT_PUBLIC_SUPABASE_URL=https://ekttjvqjkvvpavewsxhb.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_i4s7XifpKe1WVj9nAi55wg_KQ60frnZ
NEXT_PUBLIC_API_URL=https://healthier-api.inventasolutions.ai
```

**Key Difference:** The `NEXT_PUBLIC_API_URL` changes from localhost to production backend URL.

---

**Last Updated:** January 12, 2026, 8:30 PM CST  
**Status:** Ready for Deployment
