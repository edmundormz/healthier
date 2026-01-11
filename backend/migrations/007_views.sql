-- Migration: 007_views
-- Description: Helper views for common queries
-- Date: January 10, 2026

-- =============================================================================
-- ACTIVE ROUTINE ITEMS VIEW
-- =============================================================================
-- This view shows all routine items that are currently active
-- based on version dates and item expiration dates
CREATE OR REPLACE VIEW active_routine_items AS
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

-- =============================================================================
-- FAMILY DAILY SCORES VIEW
-- =============================================================================
-- This view aggregates daily scores by family
CREATE OR REPLACE VIEW family_daily_scores AS
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

-- =============================================================================
-- USER CURRENT STREAKS VIEW
-- =============================================================================
-- This view shows current streaks for all users
CREATE OR REPLACE VIEW user_current_streaks AS
SELECT 
  u.id as user_id,
  u.full_name,
  MAX(ds.current_streak) as longest_current_streak,
  COUNT(DISTINCT h.id) as active_habits_count,
  AVG(hs.current_streak) as avg_habit_streak
FROM users u
LEFT JOIN daily_snapshots ds ON u.id = ds.user_id
LEFT JOIN habits h ON u.id = h.user_id AND h.active = true
LEFT JOIN habit_streaks hs ON h.id = hs.habit_id
WHERE u.deleted_at IS NULL
GROUP BY u.id, u.full_name;

-- =============================================================================
-- WEEKLY ADHERENCE VIEW
-- =============================================================================
-- This view shows weekly adherence metrics for each user
CREATE OR REPLACE VIEW weekly_adherence AS
SELECT 
  user_id,
  DATE_TRUNC('week', snapshot_date) as week_start,
  AVG(daily_score) as avg_weekly_score,
  SUM(routines_completed) as total_routines_completed,
  SUM(routines_total) as total_routines_expected,
  CASE 
    WHEN SUM(routines_total) > 0 
    THEN (SUM(routines_completed)::NUMERIC / SUM(routines_total)::NUMERIC * 100)
    ELSE 0 
  END as routine_adherence_pct,
  SUM(habits_completed) as total_habits_completed,
  SUM(habits_total) as total_habits_expected,
  CASE 
    WHEN SUM(habits_total) > 0 
    THEN (SUM(habits_completed)::NUMERIC / SUM(habits_total)::NUMERIC * 100)
    ELSE 0 
  END as habit_adherence_pct
FROM daily_snapshots
GROUP BY user_id, DATE_TRUNC('week', snapshot_date);
