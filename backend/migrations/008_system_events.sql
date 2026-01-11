-- Migration: 008_system_events
-- Description: System events and audit log
-- Date: January 10, 2026

-- =============================================================================
-- EVENT TYPE ENUM
-- =============================================================================
CREATE TYPE event_type AS ENUM (
  'user_created',
  'routine_completed',
  'habit_logged',
  'workout_completed',
  'reward_unlocked',
  'brief_sent',
  'error_occurred'
);

-- =============================================================================
-- SYSTEM EVENTS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS system_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_type event_type NOT NULL,
  user_id UUID REFERENCES users(id),
  
  event_data JSONB,
  severity TEXT DEFAULT 'info', -- info | warning | error
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_system_events_type ON system_events(event_type);
CREATE INDEX IF NOT EXISTS idx_system_events_user ON system_events(user_id);
CREATE INDEX IF NOT EXISTS idx_system_events_created ON system_events(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_system_events_severity ON system_events(severity) WHERE severity IN ('warning', 'error');
