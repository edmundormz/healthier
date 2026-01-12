# Testing & Deployment Plan

**Date:** January 12, 2026, 4:30 PM CST  
**Status:** 🚧 Ready to Begin  
**Priority:** Testing First, Then Deployment

---

## 🎯 Strategy: Test Locally → Deploy → Test Production

**Why this order?**
1. **Catch issues early** - Fix bugs before deployment
2. **Save time** - Avoid multiple deployment iterations
3. **Build confidence** - Know it works before going live
4. **Better debugging** - Local environment is easier to debug

---

## Phase 1: Quick Manual Testing (30-60 minutes)

**Goal:** Verify core functionality works end-to-end

### 1.1 Start Both Servers

**Terminal 1 - Backend:**
```bash
cd backend
# Activate virtual environment if needed
# Windows: .\venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

uvicorn app.main:app --reload
```
✅ Backend should start at http://localhost:8000  
✅ Check http://localhost:8000/docs for API docs

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
✅ Frontend should start at http://localhost:3000

### 1.2 Test Authentication Flow

**Test Signup:**
1. Go to http://localhost:3000
2. Click "Sign Up" or navigate to `/signup`
3. Fill in form:
   - Email: `test@example.com`
   - Password: `TestPassword123!`
   - Confirm Password: `TestPassword123!`
4. Click "Sign Up"
5. ✅ Should redirect to dashboard
6. ✅ Should see user email in navbar

**Test Login:**
1. Click "Logout" button
2. Should redirect to login page
3. Enter credentials:
   - Email: `test@example.com`
   - Password: `TestPassword123!`
4. Click "Login"
5. ✅ Should redirect to dashboard

**Test Protected Routes:**
1. While logged in, try accessing:
   - `/dashboard` ✅ Should work
   - `/routines` ✅ Should work
   - `/habits` ✅ Should work
   - `/profile` ✅ Should work
2. Logout
3. Try accessing `/dashboard` directly
4. ✅ Should redirect to `/login`

### 1.3 Test CRUD Operations - Routines

**Create Routine:**
1. Navigate to `/routines`
2. Click "New Routine" button
3. Fill form:
   - Name: `Morning Vitamins`
   - Description: `Take daily vitamins`
4. Click "Create"
5. ✅ Should redirect to routine detail page
6. ✅ Should see routine name and description

**Read Routine:**
1. From routines list, click on a routine
2. ✅ Should show routine detail page
3. ✅ Should show edit and delete buttons

**Update Routine:**
1. Click "Edit" button
2. Change name to `Morning Vitamins & Supplements`
3. Click "Save"
4. ✅ Should redirect to detail page
5. ✅ Should show updated name

**Delete Routine:**
1. Click "Delete" button
2. Confirm deletion in dialog
3. ✅ Should redirect to routines list
4. ✅ Routine should be gone

### 1.4 Test CRUD Operations - Habits

**Create Habit:**
1. Navigate to `/habits`
2. Click "New Habit" button
3. Fill form:
   - Name: `Daily Steps`
   - Type: `Numeric`
   - Target Value: `10000`
   - Unit: `steps`
4. Click "Create"
5. ✅ Should redirect to habit detail page

**Read/Update/Delete Habit:**
- Follow same pattern as routines
- ✅ All operations should work

### 1.5 Test Error Scenarios

**Network Error:**
1. Stop backend server
2. Try to create a routine
3. ✅ Should show error message (not crash)

**404 Error:**
1. Navigate to `/routines/99999999` (non-existent ID)
2. ✅ Should show 404 page or error message

**Form Validation:**
1. Try to create routine with empty name
2. ✅ Should show validation error
3. ✅ Submit button should be disabled

### 1.6 Test Responsive Design

1. Open browser DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Test on:
   - Mobile (375px width)
   - Tablet (768px width)
   - Desktop (1920px width)
4. ✅ Layout should adapt properly
5. ✅ Navigation should work on mobile

---

## Phase 2: Automated Testing Setup (1-2 hours)

**Goal:** Set up automated tests for future development

### 2.1 Backend Tests (Already Partially Set Up)

**Check Current Tests:**
```bash
cd backend
pytest tests/ -v
```

**Expected Results:**
- ✅ Some tests should pass
- ⚠️ Some tests may need updating for Supabase Auth

**Update Tests for Supabase Auth:**
- Review `tests/test_supabase_auth.py`
- Update any failing tests
- Add tests for protected routes

**Run Coverage:**
```bash
pytest tests/ --cov=app --cov-report=html
```
- Target: 80% coverage for core logic
- Check `htmlcov/index.html` for coverage report

### 2.2 Frontend Tests (New Setup)

**Install Testing Dependencies:**
```bash
cd frontend
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event jest jest-environment-jsdom @types/jest
```

**Create Test Setup:**
- Create `jest.config.js`
- Create `__tests__` directory
- Write basic smoke tests for:
  - Authentication pages
  - Dashboard page
  - API client

**Run Tests:**
```bash
npm test
```

**Note:** Frontend tests are optional for MVP. Manual testing is sufficient for now.

---

## Phase 3: Deployment (1-2 hours)

**Goal:** Deploy to production (Vercel + Render)

### 3.1 Deploy Backend to Render

**Prerequisites:**
- ✅ Render account ready
- ✅ GitHub repository connected
- ✅ Environment variables documented

**Steps:**
1. Go to Render Dashboard
2. Create new Web Service
3. Connect GitHub repository
4. Configure:
   - **Name:** `ch-health-api`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3.11+
5. Set Environment Variables:
   - `DATABASE_URL` (from Supabase)
   - `DIRECT_URL` (from Supabase)
   - `SUPABASE_URL` (from Supabase)
   - `SUPABASE_SERVICE_ROLE_KEY` (from Supabase)
   - `TELEGRAM_BOT_TOKEN` (if available)
6. Deploy
7. ✅ Test health endpoint: `https://ch-health-api.onrender.com/health`

### 3.2 Deploy Frontend to Vercel

**Prerequisites:**
- ✅ Vercel account (free tier works)
- ✅ GitHub repository connected

**Steps:**
1. Go to Vercel Dashboard
2. Import GitHub repository
3. Configure:
   - **Framework Preset:** Next.js
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build` (default)
   - **Output Directory:** `.next` (default)
4. Set Environment Variables:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `NEXT_PUBLIC_API_URL` (Render backend URL)
5. Deploy
6. ✅ Test frontend: `https://your-app.vercel.app`

### 3.3 Update Frontend API URL

**After Backend Deployment:**
1. Get Render backend URL (e.g., `https://ch-health-api.onrender.com`)
2. Update Vercel environment variable:
   - `NEXT_PUBLIC_API_URL` = `https://ch-health-api.onrender.com`
3. Redeploy frontend (or wait for auto-deploy)

### 3.4 Test Production Deployment

**Test Production:**
1. Visit production frontend URL
2. Test signup/login
3. Test CRUD operations
4. ✅ Everything should work as in local

**Common Issues:**
- CORS errors → Check backend CORS settings
- 401 errors → Check JWT token handling
- Database connection → Check Render environment variables

---

## Phase 4: Post-Deployment Testing (30 minutes)

**Goal:** Verify production works correctly

### 4.1 Production Smoke Tests

1. **Authentication:**
   - Signup new user
   - Login
   - Logout
   - ✅ All should work

2. **CRUD Operations:**
   - Create routine
   - Create habit
   - Edit both
   - Delete both
   - ✅ All should work

3. **Error Handling:**
   - Test 404 pages
   - Test network errors
   - ✅ Should show user-friendly errors

### 4.2 Performance Check

1. Check page load times
2. Check API response times
3. ✅ Should be reasonable (< 2s for page loads)

---

## 📊 Testing Checklist

### Manual Testing
- [ ] Backend server starts
- [ ] Frontend server starts
- [ ] Signup works
- [ ] Login works
- [ ] Logout works
- [ ] Protected routes redirect correctly
- [ ] Create routine works
- [ ] Read routine works
- [ ] Update routine works
- [ ] Delete routine works
- [ ] Create habit works
- [ ] Read habit works
- [ ] Update habit works
- [ ] Delete habit works
- [ ] Form validation works
- [ ] Error handling works
- [ ] Responsive design works

### Automated Testing
- [ ] Backend tests pass
- [ ] Backend test coverage > 80%
- [ ] Frontend tests pass (optional)

### Deployment
- [ ] Backend deployed to Render
- [ ] Frontend deployed to Vercel
- [ ] Environment variables set
- [ ] Production health check passes
- [ ] Production signup/login works
- [ ] Production CRUD operations work

---

## 🚨 Troubleshooting

### Backend Won't Start
- Check Python version (need 3.11+)
- Check virtual environment activated
- Check `.env` file exists with correct values
- Check database connection

### Frontend Won't Start
- Check Node.js version (need 18+)
- Run `npm install` again
- Check `.env.local` file exists
- Check for TypeScript errors

### API Calls Fail
- Check backend is running
- Check `NEXT_PUBLIC_API_URL` is correct
- Check CORS settings in backend
- Check browser console for errors

### Authentication Fails
- Check Supabase credentials
- Check JWT token in browser DevTools
- Check Supabase Auth settings
- Check backend JWT validation

---

## 🎯 Success Criteria

**Ready to Deploy When:**
- ✅ All manual tests pass
- ✅ No console errors
- ✅ Forms work correctly
- ✅ API integration works
- ✅ Error handling works

**Deployment Successful When:**
- ✅ Both services deployed
- ✅ Production tests pass
- ✅ No critical errors
- ✅ Performance acceptable

---

## 📝 Next Steps After Deployment

1. **Monitor Production:**
   - Check Render logs
   - Check Vercel logs
   - Monitor error rates

2. **Continue Development:**
   - Rules Engine (Phase 2)
   - Telegram Bot (Phase 3)
   - LangGraph + Vita (Phase 4)

3. **Improve Testing:**
   - Add more backend tests
   - Set up frontend tests
   - Add E2E tests (optional)

---

**Last Updated:** January 12, 2026, 4:30 PM CST  
**Status:** Ready to Begin Testing
