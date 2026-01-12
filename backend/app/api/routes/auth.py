"""
Authentication API Routes

⚠️ DEPRECATED: This module is kept for reference but is no longer used.

Supabase Auth now handles:
- User registration (signup) - Use Supabase client on frontend
- User login - Use Supabase client on frontend
- Token generation - Supabase generates JWT tokens
- Password reset - Built into Supabase Auth
- Email verification - Built into Supabase Auth

Backend only needs to:
- Validate Supabase JWT tokens (see `app/core/dependencies.py`)
- Sync users from auth.users to public.users (automatic)

Migration Notes:
- Custom signup/login endpoints have been removed
- Use Supabase client on frontend for authentication
- Backend validates tokens automatically via `get_current_user` dependency

See: `SUPABASE_AUTH_MIGRATION.md` for migration details.
See: https://supabase.com/docs/guides/auth for Supabase Auth docs.
"""

from fastapi import APIRouter

# Create router with prefix and tags
router = APIRouter(prefix="/auth", tags=["authentication"])

# =============================================================================
# Authentication Endpoints
# =============================================================================
# 
# NOTE: These endpoints have been removed in favor of Supabase Auth.
# 
# To sign up users, use Supabase client on the frontend:
# ```typescript
# const { data, error } = await supabase.auth.signUp({
#   email: 'user@example.com',
#   password: 'password',
#   options: {
#     data: { full_name: 'John Doe', language: 'en' }
#   }
# })
# ```
#
# To log in users, use Supabase client on the frontend:
# ```typescript
# const { data, error } = await supabase.auth.signInWithPassword({
#   email: 'user@example.com',
#   password: 'password'
# })
# ```
#
# To use authenticated endpoints, include the Supabase token:
# ```typescript
# const { data: { session } } = await supabase.auth.getSession()
# const token = session?.access_token
#
# fetch('/api/routines/', {
#   headers: { 'Authorization': `Bearer ${token}` }
# })
# ```
#
# Backend automatically:
# 1. Validates Supabase JWT token
# 2. Syncs user from auth.users to public.users if needed
# 3. Injects current_user into route handler
#
# See: SUPABASE_AUTH_MIGRATION.md for complete migration guide.
