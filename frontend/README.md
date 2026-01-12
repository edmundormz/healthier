# CH Health OS — Frontend

**Next.js 16.1.1** frontend application for CH Health OS.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Set Up Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```bash
# Supabase Configuration (Public Keys - Safe for Browser)
NEXT_PUBLIC_SUPABASE_URL=https://ekttjvqjkvvpavewsxhb.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_i4s7XifpKe1WVj9nAi55wg_KQ60frnZ

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Note:** These keys are already configured in the backend's `ENV_REFERENCE.md`. Copy them from there.

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📁 Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── (auth)/            # Auth routes (login, signup)
├── lib/
│   ├── supabase/          # Supabase client utilities
│   │   ├── client.ts      # Client Component client
│   │   ├── server.ts      # Server Component client
│   │   └── middleware.ts  # Middleware client
│   └── api/
│       └── client.ts      # Backend API client
└── components/            # React components (to be created)
```

## 🔧 Key Features

### Supabase Integration

- **Client Components**: Use `@/lib/supabase/client`
- **Server Components**: Use `@/lib/supabase/server`
- **Middleware**: Automatic session refresh

### API Clients

**Server Components** (use `@/lib/api/server`):
```typescript
import api from '@/lib/api/server';

// In Server Components
const routines = await api.get('/api/routines/');
```

**Client Components** (use `@/lib/api/client`):
```typescript
'use client';
import api from '@/lib/api/client';

// In Client Components
const routines = await api.get('/api/routines/');
```

Both clients automatically:
- Add Supabase JWT tokens to requests
- Handle authentication errors (401, 403)
- Provide type-safe responses

## 🎯 What's Built

1. ✅ Next.js 16.1.1 installed
2. ✅ Supabase clients configured (client, server, middleware)
3. ✅ API clients created (client-side and server-side)
4. ✅ Authentication pages (login, signup, logout)
5. ✅ Protected route middleware and session management
6. ✅ Core views (dashboard, routines, habits, profile)
7. ✅ Navigation bar with user info
8. ✅ Home page with auth redirect

## 📁 Complete Structure

```
frontend/
├── app/
│   ├── (auth)/              # Auth routes (login, signup)
│   │   ├── login/
│   │   └── signup/
│   ├── dashboard/          # Dashboard (protected)
│   ├── routines/            # Routines (protected)
│   │   ├── [id]/           # Routine detail
│   │   └── page.tsx        # Routines list
│   ├── habits/              # Habits (protected)
│   │   ├── [id]/           # Habit detail
│   │   └── page.tsx        # Habits list
│   ├── profile/             # User profile (protected)
│   ├── layout.tsx          # Root layout
│   └── page.tsx            # Home page
├── components/
│   ├── auth/
│   │   └── LogoutButton.tsx
│   └── layout/
│       └── Navbar.tsx
├── lib/
│   ├── supabase/           # Supabase clients
│   │   ├── client.ts      # Client Component client
│   │   ├── server.ts      # Server Component client
│   │   └── middleware.ts  # Middleware client
│   ├── api/
│   │   ├── client.ts      # Client-side API client
│   │   └── server.ts      # Server-side API client
│   └── auth/
│       ├── actions.ts      # Server actions (logout)
│       └── utils.ts        # Auth utilities (requireAuth)
└── middleware.ts           # Next.js middleware
```

## 📚 Documentation

- [Next.js Documentation](https://nextjs.org/docs)
- [Supabase Auth Guide](https://supabase.com/docs/guides/auth)
- [Backend API Docs](../backend/README.md)
