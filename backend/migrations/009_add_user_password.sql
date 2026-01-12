-- Migration: 009_add_user_password
-- Description: Add password field to users table for authentication
-- Date: January 11, 2026

-- =============================================================================
-- ADD PASSWORD FIELD TO USERS TABLE
-- =============================================================================

-- Add hashed_password column to users table
-- This field is nullable to support:
-- 1. Existing users (who may not have passwords yet)
-- 2. Optional authentication methods (e.g., Supabase Auth, OAuth)
-- 3. Migration from other auth systems

ALTER TABLE users
ADD COLUMN IF NOT EXISTS hashed_password TEXT;

-- Add comment explaining the field
COMMENT ON COLUMN users.hashed_password IS 
  'Bcrypt-hashed password. Never store plain text passwords. Nullable to support existing users and optional auth methods.';

-- Note: No index needed on password field (we query by email, not password)
-- The password field is only used for verification, not lookup
