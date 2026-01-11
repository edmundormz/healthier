-- Migration: 002_routines
-- Description: Routine system (routines, versions, cards, items, completions)
-- Date: January 10, 2026

-- =============================================================================
-- ENUMS
-- =============================================================================
CREATE TYPE moment_of_day AS ENUM ('MORNING', 'MIDDAY', 'EVENING', 'NIGHT');

CREATE TYPE routine_item_type AS ENUM (
  'medication',
  'supplement',
  'skincare',
  'hair_care',
  'habit'
);

-- =============================================================================
-- ROUTINES TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS routines (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL, -- "Morning Routine"
  description TEXT,
  active_version_id UUID, -- FK to routine_versions (added later)
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_routines_user ON routines(user_id);

-- Apply updated_at trigger
CREATE TRIGGER update_routines_updated_at BEFORE UPDATE ON routines
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- ROUTINE VERSIONS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS routine_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  routine_id UUID NOT NULL REFERENCES routines(id) ON DELETE CASCADE,
  version_number INT NOT NULL DEFAULT 1,
  
  start_date DATE NOT NULL,
  end_date DATE, -- NULL = ongoing
  
  created_by UUID REFERENCES users(id),
  notes TEXT, -- "New protocol from Dr. Smith"
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(routine_id, version_number)
);

CREATE INDEX IF NOT EXISTS idx_routine_versions_routine ON routine_versions(routine_id);
CREATE INDEX IF NOT EXISTS idx_routine_versions_dates ON routine_versions(start_date, end_date);

-- Now we can add the foreign key constraint to routines.active_version_id
-- Note: This creates a circular reference, but it's intentional and safe
ALTER TABLE routines 
ADD CONSTRAINT fk_routines_active_version 
FOREIGN KEY (active_version_id) REFERENCES routine_versions(id) ON DELETE SET NULL;

-- =============================================================================
-- ROUTINE CARDS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS routine_cards (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  routine_version_id UUID NOT NULL REFERENCES routine_versions(id) ON DELETE CASCADE,
  moment moment_of_day NOT NULL,
  sort_order INT DEFAULT 0,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_routine_cards_version ON routine_cards(routine_version_id);

-- =============================================================================
-- ROUTINE ITEMS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS routine_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  routine_card_id UUID NOT NULL REFERENCES routine_cards(id) ON DELETE CASCADE,
  
  type routine_item_type NOT NULL,
  name TEXT NOT NULL, -- "Metformin"
  dosage TEXT, -- "500mg"
  instructions TEXT, -- "Take with breakfast"
  
  frequency TEXT DEFAULT 'daily', -- daily | weekdays | custom
  
  -- Expiration logic
  expires_at DATE, -- NULL = never expires
  duration_days INT, -- Alternative to expires_at
  
  -- Transition logic
  next_item_id UUID REFERENCES routine_items(id),
  
  sort_order INT DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_routine_items_card ON routine_items(routine_card_id);
CREATE INDEX IF NOT EXISTS idx_routine_items_expiration ON routine_items(expires_at);

-- =============================================================================
-- ROUTINE COMPLETIONS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS routine_completions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  routine_item_id UUID NOT NULL REFERENCES routine_items(id),
  
  completed_at TIMESTAMPTZ DEFAULT NOW(),
  completion_date DATE NOT NULL DEFAULT CURRENT_DATE,
  
  notes TEXT,
  skipped BOOLEAN DEFAULT false,
  skip_reason TEXT,
  
  UNIQUE(user_id, routine_item_id, completion_date)
);

CREATE INDEX IF NOT EXISTS idx_routine_completions_user_date ON routine_completions(user_id, completion_date);
CREATE INDEX IF NOT EXISTS idx_routine_completions_item ON routine_completions(routine_item_id);
