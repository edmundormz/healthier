# CH Health OS — Complete Database Schema v0

**Database:** PostgreSQL 15+ (Supabase)  
**Timezone:** All timestamps in UTC, display in America/Chicago

---

## Schema Overview

### Core Entities
- `users` — Individual users (Candy, Héctor)
- `families` — Family groups (Family CH)
- `family_memberships` — Links users to families

### Routine System
- `routines` — Container for routine versions
- `routine_versions` — Time-bound routine definitions
- `routine_cards` — Groups items by moment of day
- `routine_items` — Individual tasks (meds, supplements, habits)
- `routine_completions` — Daily check-ins

### Habits
- `habits` — Habit definitions
- `habit_logs` — Daily habit completions
- `habit_streaks` — Calculated streak data

### Exercise
- `workout_plans` — User workout plans
- `workout_sessions` — A/B/C sessions
- `exercises` — Exercise library
- `workout_exercises` — Exercises in a session
- `workout_logs` — Completed workouts with RPE

### Body Metrics
- `body_metrics` — Weekly body composition data

### Scoring & Gamification
- `daily_snapshots` — Daily health summary
- `rewards` — Reward definitions
- `reward_rules` — Conditions for unlocking
- `reward_unlocks` — Unlocked rewards log

### Telegram
- `telegram_users` — Telegram ID mapping
- `telegram_messages` — Message history

### AI/Conversations
- `conversation_sessions` — Active conversation state
- `langgraph_checkpoints` — LangGraph state (auto-managed)

### System
- `system_events` — Audit log

---

## Detailed Schema

### users
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  full_name TEXT NOT NULL,
  timezone TEXT DEFAULT 'America/Chicago',
  
  -- Preferences
  language TEXT DEFAULT 'es', -- es | en
  notification_enabled BOOLEAN DEFAULT true,
  
  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  last_active_at TIMESTAMPTZ,
  
  -- Soft delete
  deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_deleted ON users(deleted_at) WHERE deleted_at IS NULL;
```

---

### families
```sql
CREATE TABLE families (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL, -- "Family CH"
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

### family_memberships
```sql
CREATE TABLE family_memberships (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  family_id UUID NOT NULL REFERENCES families(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role TEXT DEFAULT 'member', -- admin | member
  joined_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(family_id, user_id)
);

CREATE INDEX idx_family_memberships_family ON family_memberships(family_id);
CREATE INDEX idx_family_memberships_user ON family_memberships(user_id);
```

---

## Routine System

### routines
```sql
CREATE TABLE routines (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL, -- "Morning Routine"
  description TEXT,
  active_version_id UUID, -- FK to routine_versions
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_routines_user ON routines(user_id);
```

---

### routine_versions
```sql
CREATE TABLE routine_versions (
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

CREATE INDEX idx_routine_versions_routine ON routine_versions(routine_id);
CREATE INDEX idx_routine_versions_dates ON routine_versions(start_date, end_date);
```

---

### routine_cards
```sql
CREATE TYPE moment_of_day AS ENUM ('MORNING', 'MIDDAY', 'EVENING', 'NIGHT');

CREATE TABLE routine_cards (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  routine_version_id UUID NOT NULL REFERENCES routine_versions(id) ON DELETE CASCADE,
  moment moment_of_day NOT NULL,
  sort_order INT DEFAULT 0,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_routine_cards_version ON routine_cards(routine_version_id);
```

---

### routine_items
```sql
CREATE TYPE routine_item_type AS ENUM (
  'medication',
  'supplement',
  'skincare',
  'hair_care',
  'habit'
);

CREATE TABLE routine_items (
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

CREATE INDEX idx_routine_items_card ON routine_items(routine_card_id);
CREATE INDEX idx_routine_items_expiration ON routine_items(expires_at);
```

---

### routine_completions
```sql
CREATE TABLE routine_completions (
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

CREATE INDEX idx_routine_completions_user_date ON routine_completions(user_id, completion_date);
CREATE INDEX idx_routine_completions_item ON routine_completions(routine_item_id);
```

---

## Habits

### habits
```sql
CREATE TYPE habit_type AS ENUM ('boolean', 'numeric');

CREATE TABLE habits (
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

CREATE INDEX idx_habits_user ON habits(user_id);
CREATE INDEX idx_habits_active ON habits(active) WHERE active = true;
```

---

### habit_logs
```sql
CREATE TABLE habit_logs (
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

CREATE INDEX idx_habit_logs_habit_date ON habit_logs(habit_id, log_date DESC);
CREATE INDEX idx_habit_logs_user_date ON habit_logs(user_id, log_date DESC);
```

---

### habit_streaks
```sql
CREATE TABLE habit_streaks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  habit_id UUID NOT NULL REFERENCES habits(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id),
  
  current_streak INT DEFAULT 0,
  longest_streak INT DEFAULT 0,
  last_completed_date DATE,
  
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(habit_id, user_id)
);

CREATE INDEX idx_habit_streaks_user ON habit_streaks(user_id);
```

---

## Exercise System

### workout_plans
```sql
CREATE TYPE workout_goal AS ENUM ('fat_loss', 'recomposition', 'energy', 'strength');

CREATE TABLE workout_plans (
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

CREATE INDEX idx_workout_plans_user ON workout_plans(user_id);
```

---

### workout_sessions
```sql
CREATE TABLE workout_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workout_plan_id UUID NOT NULL REFERENCES workout_plans(id) ON DELETE CASCADE,
  
  name TEXT NOT NULL, -- "Session A - Upper Body"
  session_label TEXT, -- "A" | "B" | "C"
  description TEXT,
  
  sort_order INT DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_workout_sessions_plan ON workout_sessions(workout_plan_id);
```

---

### exercises
```sql
CREATE TABLE exercises (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE, -- "Dumbbell Bench Press"
  description TEXT,
  muscle_groups TEXT[], -- ["chest", "triceps"]
  equipment TEXT[], -- ["dumbbells"]
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_exercises_name ON exercises(name);
```

---

### workout_exercises
```sql
CREATE TABLE workout_exercises (
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

CREATE INDEX idx_workout_exercises_session ON workout_exercises(workout_session_id);
```

---

### workout_logs
```sql
CREATE TABLE workout_logs (
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

CREATE INDEX idx_workout_logs_user_date ON workout_logs(user_id, completion_date DESC);
```

---

## Body Metrics

### body_metrics
```sql
CREATE TABLE body_metrics (
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

CREATE INDEX idx_body_metrics_user_date ON body_metrics(user_id, measurement_date DESC);
```

---

## Scoring & Gamification

### daily_snapshots
```sql
CREATE TABLE daily_snapshots (
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

CREATE INDEX idx_daily_snapshots_user_date ON daily_snapshots(user_id, snapshot_date DESC);
```

---

### rewards
```sql
CREATE TABLE rewards (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  family_id UUID REFERENCES families(id), -- NULL = individual
  user_id UUID REFERENCES users(id), -- NULL = family reward
  
  name TEXT NOT NULL, -- "Friday Steak & Wine Night"
  description TEXT,
  category TEXT, -- "food" | "experience" | "rest"
  
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_rewards_family ON rewards(family_id);
CREATE INDEX idx_rewards_user ON rewards(user_id);
```

---

### reward_rules
```sql
CREATE TABLE reward_rules (
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

CREATE INDEX idx_reward_rules_reward ON reward_rules(reward_id);
```

---

### reward_unlocks
```sql
CREATE TABLE reward_unlocks (
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

CREATE INDEX idx_reward_unlocks_user ON reward_unlocks(user_id);
CREATE INDEX idx_reward_unlocks_family ON reward_unlocks(family_id);
CREATE INDEX idx_reward_unlocks_date ON reward_unlocks(unlock_date DESC);
```

---

## Telegram Integration

### telegram_users
```sql
CREATE TABLE telegram_users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  telegram_user_id BIGINT NOT NULL UNIQUE,
  telegram_username TEXT,
  
  first_name TEXT,
  last_name TEXT,
  
  linked_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(user_id) -- One telegram per user
);

CREATE INDEX idx_telegram_users_telegram_id ON telegram_users(telegram_user_id);
CREATE INDEX idx_telegram_users_user ON telegram_users(user_id);
```

---

### telegram_messages
```sql
CREATE TABLE telegram_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  telegram_user_id BIGINT NOT NULL,
  user_id UUID REFERENCES users(id),
  
  direction TEXT NOT NULL, -- "inbound" | "outbound"
  message_text TEXT,
  message_data JSONB, -- Full Telegram message object
  
  received_at TIMESTAMPTZ DEFAULT NOW(),
  sent_at TIMESTAMPTZ
);

CREATE INDEX idx_telegram_messages_telegram_user ON telegram_messages(telegram_user_id);
CREATE INDEX idx_telegram_messages_user_received ON telegram_messages(user_id, received_at DESC);
```

---

## AI / Conversations

### conversation_sessions
```sql
CREATE TABLE conversation_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  
  context JSONB DEFAULT '[]'::jsonb, -- Last N messages
  session_metadata JSONB DEFAULT '{}'::jsonb,
  
  last_message_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ DEFAULT NOW() + INTERVAL '1 hour',
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_conversation_sessions_user ON conversation_sessions(user_id);
CREATE INDEX idx_conversation_sessions_expires ON conversation_sessions(expires_at);
```

---

### langgraph_checkpoints
```sql
-- Auto-managed by LangGraph PostgresSaver
-- Schema defined by LangGraph
-- Stores workflow state, thread history, etc.
```

---

## System

### system_events
```sql
CREATE TYPE event_type AS ENUM (
  'user_created',
  'routine_completed',
  'habit_logged',
  'workout_completed',
  'reward_unlocked',
  'brief_sent',
  'error_occurred'
);

CREATE TABLE system_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_type event_type NOT NULL,
  user_id UUID REFERENCES users(id),
  
  event_data JSONB,
  severity TEXT DEFAULT 'info', -- info | warning | error
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_system_events_type ON system_events(event_type);
CREATE INDEX idx_system_events_user ON system_events(user_id);
CREATE INDEX idx_system_events_created ON system_events(created_at DESC);
```

---

## Helper Views

### active_routine_items_view
```sql
CREATE VIEW active_routine_items AS
SELECT 
  ri.*,
  rc.moment,
  rv.start_date as version_start_date,
  rv.end_date as version_end_date,
  r.user_id
FROM routine_items ri
JOIN routine_cards rc ON ri.routine_card_id = rc.id
JOIN routine_versions rv ON rc.routine_version_id = rv.id
JOIN routines r ON rv.routine_id = r.id
WHERE 
  CURRENT_DATE >= rv.start_date
  AND (rv.end_date IS NULL OR CURRENT_DATE <= rv.end_date)
  AND (ri.expires_at IS NULL OR CURRENT_DATE <= ri.expires_at);
```

---

### family_daily_scores_view
```sql
CREATE VIEW family_daily_scores AS
SELECT 
  fm.family_id,
  ds.snapshot_date,
  AVG(ds.daily_score) as family_score,
  SUM(ds.routines_completed) as family_routines_completed,
  SUM(ds.habits_completed) as family_habits_completed
FROM daily_snapshots ds
JOIN users u ON ds.user_id = u.id
JOIN family_memberships fm ON u.id = fm.user_id
GROUP BY fm.family_id, ds.snapshot_date;
```

---

## Row Level Security (RLS) Policies

### Enable RLS on all tables
```sql
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE families ENABLE ROW LEVEL SECURITY;
ALTER TABLE family_memberships ENABLE ROW LEVEL SECURITY;
ALTER TABLE routines ENABLE ROW LEVEL SECURITY;
-- ... (enable on all user-facing tables)
```

---

### Example Policies

**Users can only see their own data:**
```sql
CREATE POLICY "Users can view own data"
ON users FOR SELECT
USING (auth.uid() = id);

CREATE POLICY "Users can update own data"
ON users FOR UPDATE
USING (auth.uid() = id);
```

**Family members can see family data:**
```sql
CREATE POLICY "Family members can view family data"
ON families FOR SELECT
USING (
  id IN (
    SELECT family_id 
    FROM family_memberships 
    WHERE user_id = auth.uid()
  )
);
```

**Users can only see their own routines:**
```sql
CREATE POLICY "Users can manage own routines"
ON routines FOR ALL
USING (user_id = auth.uid());
```

**Service role bypasses RLS:**
```sql
-- Backend API uses service_role key
-- No RLS policies needed for service role
```

---

## Indexes Summary

All critical indexes included above in table definitions.

**Additional composite indexes if needed:**
```sql
-- For frequent queries
CREATE INDEX idx_routine_completions_lookup 
ON routine_completions(user_id, completion_date, routine_item_id);

CREATE INDEX idx_habit_logs_lookup 
ON habit_logs(user_id, log_date, habit_id);
```

---

## Migration Strategy

1. **001_initial_schema.sql** — Core tables (users, families)
2. **002_routines.sql** — Routine system
3. **003_habits_exercise.sql** — Habits + exercise
4. **004_scoring_rewards.sql** — Scoring + gamification
5. **005_telegram.sql** — Telegram integration
6. **006_ai_sessions.sql** — Conversation state
7. **007_views.sql** — Helper views
8. **008_rls_policies.sql** — Row level security
9. **009_seed_data.sql** — Initial dev/test data

---

**Schema Status:** Ready for implementation ✓
