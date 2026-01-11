-- Migration: 004_scoring_rewards
-- Description: Scoring and gamification system
-- Date: January 10, 2026

-- =============================================================================
-- DAILY SNAPSHOTS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS daily_snapshots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  snapshot_date DATE NOT NULL,
  
  -- Scores (0-100)
  daily_score NUMERIC DEFAULT 0,
  routine_score NUMERIC DEFAULT 0,
  habit_score NUMERIC DEFAULT 0,
  exercise_score NUMERIC DEFAULT 0,
  
  -- Adherence
  routines_completed INT DEFAULT 0,
  routines_total INT DEFAULT 0,
  habits_completed INT DEFAULT 0,
  habits_total INT DEFAULT 0,
  
  -- Streaks
  current_streak INT DEFAULT 0,
  
  generated_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(user_id, snapshot_date)
);

CREATE INDEX IF NOT EXISTS idx_daily_snapshots_user_date ON daily_snapshots(user_id, snapshot_date DESC);

-- =============================================================================
-- REWARDS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS rewards (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  family_id UUID REFERENCES families(id), -- NULL = individual
  user_id UUID REFERENCES users(id), -- NULL = family reward
  
  name TEXT NOT NULL, -- "Friday Steak & Wine Night"
  description TEXT,
  category TEXT, -- "food" | "experience" | "rest"
  
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_rewards_family ON rewards(family_id);
CREATE INDEX IF NOT EXISTS idx_rewards_user ON rewards(user_id);

-- =============================================================================
-- REWARD RULES TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS reward_rules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  reward_id UUID NOT NULL REFERENCES rewards(id) ON DELETE CASCADE,
  
  -- Conditions (JSON for flexibility)
  conditions JSONB NOT NULL,
  /* Example:
  {
    "family_weekly_score_min": 85,
    "walk_streak_min": 4,
    "routine_adherence_min": 80
  }
  */
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_reward_rules_reward ON reward_rules(reward_id);

-- =============================================================================
-- REWARD UNLOCKS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS reward_unlocks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  reward_id UUID NOT NULL REFERENCES rewards(id),
  user_id UUID REFERENCES users(id), -- NULL if family reward
  family_id UUID REFERENCES families(id),
  
  unlocked_at TIMESTAMPTZ DEFAULT NOW(),
  unlock_date DATE DEFAULT CURRENT_DATE,
  
  used BOOLEAN DEFAULT false,
  used_at TIMESTAMPTZ,
  
  notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_reward_unlocks_user ON reward_unlocks(user_id);
CREATE INDEX IF NOT EXISTS idx_reward_unlocks_family ON reward_unlocks(family_id);
CREATE INDEX IF NOT EXISTS idx_reward_unlocks_date ON reward_unlocks(unlock_date DESC);
