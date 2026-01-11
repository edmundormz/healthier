-- Migration: 003_habits_exercise
-- Description: Habits and exercise system
-- Date: January 10, 2026

-- =============================================================================
-- ENUMS
-- =============================================================================
CREATE TYPE habit_type AS ENUM ('boolean', 'numeric');
CREATE TYPE workout_goal AS ENUM ('fat_loss', 'recomposition', 'energy', 'strength');

-- =============================================================================
-- HABITS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS habits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  name TEXT NOT NULL, -- "Walk 10k steps"
  type habit_type DEFAULT 'boolean',
  
  target_value NUMERIC, -- For numeric habits
  unit TEXT, -- "steps" | "glasses" | "minutes"
  
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_habits_user ON habits(user_id);
CREATE INDEX IF NOT EXISTS idx_habits_active ON habits(active) WHERE active = true;

-- Apply updated_at trigger
CREATE TRIGGER update_habits_updated_at BEFORE UPDATE ON habits
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- HABIT LOGS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS habit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  habit_id UUID NOT NULL REFERENCES habits(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id),
  
  log_date DATE NOT NULL DEFAULT CURRENT_DATE,
  completed BOOLEAN DEFAULT false,
  value NUMERIC, -- For numeric habits
  
  logged_at TIMESTAMPTZ DEFAULT NOW(),
  notes TEXT,
  
  UNIQUE(habit_id, log_date)
);

CREATE INDEX IF NOT EXISTS idx_habit_logs_habit_date ON habit_logs(habit_id, log_date DESC);
CREATE INDEX IF NOT EXISTS idx_habit_logs_user_date ON habit_logs(user_id, log_date DESC);

-- =============================================================================
-- HABIT STREAKS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS habit_streaks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  habit_id UUID NOT NULL REFERENCES habits(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id),
  
  current_streak INT DEFAULT 0,
  longest_streak INT DEFAULT 0,
  last_completed_date DATE,
  
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(habit_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_habit_streaks_user ON habit_streaks(user_id);

-- Apply updated_at trigger
CREATE TRIGGER update_habit_streaks_updated_at BEFORE UPDATE ON habit_streaks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- WORKOUT PLANS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS workout_plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  name TEXT NOT NULL, -- "3-Day Upper/Lower Split"
  goal workout_goal NOT NULL,
  
  days_per_week INT DEFAULT 3,
  available_equipment TEXT[], -- ["dumbbells", "resistance_bands"]
  
  active BOOLEAN DEFAULT true,
  start_date DATE DEFAULT CURRENT_DATE,
  end_date DATE,
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_workout_plans_user ON workout_plans(user_id);

-- Apply updated_at trigger
CREATE TRIGGER update_workout_plans_updated_at BEFORE UPDATE ON workout_plans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- WORKOUT SESSIONS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS workout_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workout_plan_id UUID NOT NULL REFERENCES workout_plans(id) ON DELETE CASCADE,
  
  name TEXT NOT NULL, -- "Session A - Upper Body"
  session_label TEXT, -- "A" | "B" | "C"
  description TEXT,
  
  sort_order INT DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_workout_sessions_plan ON workout_sessions(workout_plan_id);

-- =============================================================================
-- EXERCISES TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS exercises (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE, -- "Dumbbell Bench Press"
  description TEXT,
  muscle_groups TEXT[], -- ["chest", "triceps"]
  equipment TEXT[], -- ["dumbbells"]
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_exercises_name ON exercises(name);

-- =============================================================================
-- WORKOUT EXERCISES TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS workout_exercises (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workout_session_id UUID NOT NULL REFERENCES workout_sessions(id) ON DELETE CASCADE,
  exercise_id UUID NOT NULL REFERENCES exercises(id),
  
  sets INT NOT NULL DEFAULT 3,
  reps TEXT, -- "8-12" | "AMRAP" | "12"
  load_kg NUMERIC,
  rpe_target NUMERIC, -- 1-10 scale
  
  rest_seconds INT DEFAULT 90,
  notes TEXT,
  
  sort_order INT DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_workout_exercises_session ON workout_exercises(workout_session_id);

-- =============================================================================
-- WORKOUT LOGS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS workout_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  workout_session_id UUID NOT NULL REFERENCES workout_sessions(id),
  
  completed_at TIMESTAMPTZ DEFAULT NOW(),
  completion_date DATE DEFAULT CURRENT_DATE,
  
  rpe_actual NUMERIC, -- Overall session RPE
  duration_minutes INT,
  notes TEXT, -- "Felt strong" | "Lower back pain"
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_workout_logs_user_date ON workout_logs(user_id, completion_date DESC);

-- =============================================================================
-- BODY METRICS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS body_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  measurement_date DATE NOT NULL,
  week_of_year INT, -- Derived: EXTRACT(WEEK FROM measurement_date)
  
  -- Core metrics
  weight_kg NUMERIC,
  body_fat_pct NUMERIC,
  muscle_mass_kg NUMERIC,
  
  -- Optional
  waist_cm NUMERIC,
  visceral_fat NUMERIC,
  
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(user_id, measurement_date)
);

CREATE INDEX IF NOT EXISTS idx_body_metrics_user_date ON body_metrics(user_id, measurement_date DESC);
