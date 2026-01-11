-- Migration: 005_telegram
-- Description: Telegram integration tables
-- Date: January 10, 2026

-- =============================================================================
-- TELEGRAM USERS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS telegram_users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  telegram_user_id BIGINT NOT NULL UNIQUE,
  telegram_username TEXT,
  
  first_name TEXT,
  last_name TEXT,
  
  linked_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(user_id) -- One telegram per user
);

CREATE INDEX IF NOT EXISTS idx_telegram_users_telegram_id ON telegram_users(telegram_user_id);
CREATE INDEX IF NOT EXISTS idx_telegram_users_user ON telegram_users(user_id);

-- =============================================================================
-- TELEGRAM MESSAGES TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS telegram_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  telegram_user_id BIGINT NOT NULL,
  user_id UUID REFERENCES users(id),
  
  direction TEXT NOT NULL, -- "inbound" | "outbound"
  message_text TEXT,
  message_data JSONB, -- Full Telegram message object
  
  received_at TIMESTAMPTZ DEFAULT NOW(),
  sent_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_telegram_messages_telegram_user ON telegram_messages(telegram_user_id);
CREATE INDEX IF NOT EXISTS idx_telegram_messages_user_received ON telegram_messages(user_id, received_at DESC);
