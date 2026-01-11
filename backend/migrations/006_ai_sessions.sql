-- Migration: 006_ai_sessions
-- Description: AI conversation sessions and LangGraph checkpoints
-- Date: January 10, 2026

-- =============================================================================
-- CONVERSATION SESSIONS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS conversation_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  
  context JSONB DEFAULT '[]'::jsonb, -- Last N messages
  session_metadata JSONB DEFAULT '{}'::jsonb,
  
  last_message_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ DEFAULT NOW() + INTERVAL '1 hour',
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_conversation_sessions_user ON conversation_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_conversation_sessions_expires ON conversation_sessions(expires_at);

-- =============================================================================
-- LANGGRAPH CHECKPOINTS TABLE
-- =============================================================================
-- Note: This table structure is managed by LangGraph's PostgresSaver
-- We create it here for completeness, but LangGraph will manage it
-- See: https://langchain-ai.github.io/langgraph/reference/checkpoints/#postgresqlsaver

-- LangGraph will create these tables automatically when initialized:
-- - checkpoints: Stores workflow state
-- - checkpoint_writes: Stores intermediate writes
-- - checkpoint_blobs: Stores large binary data

-- If you need to manually create them, use LangGraph's schema:
-- from langgraph.checkpoint.postgres import PostgresSaver
-- PostgresSaver.create_tables(connection)

-- For now, we'll let LangGraph manage its own tables
-- This migration file serves as documentation of the AI session tables
