# Database Migrations

This directory contains SQL migration files for the CH Health OS database.

## Migration Order

Migrations must be applied in order:

1. **001_initial_schema.sql** - Core tables (users, families, memberships)
2. **002_routines.sql** - Routine system
3. **003_habits_exercise.sql** - Habits and exercise tracking
4. **004_scoring_rewards.sql** - Scoring and gamification
5. **005_telegram.sql** - Telegram integration
6. **006_ai_sessions.sql** - AI conversation sessions
7. **007_views.sql** - Helper views
8. **008_system_events.sql** - System events and audit log

## Applying Migrations

### Using Supabase MCP (Recommended)

The migrations are applied via the Supabase MCP connection:

```python
# Migrations are applied automatically via MCP
# See: backend/DATABASE_SETUP.md
```

### Manual Application

If needed, you can apply migrations manually:

1. Go to: https://supabase.com/dashboard/project/ekttjvqjkvvpavewsxhb/editor
2. Open the SQL Editor
3. Copy and paste each migration file
4. Execute in order (001 → 008)

## Migration Status

Track which migrations have been applied:

```sql
-- Check if a table exists
SELECT EXISTS (
  SELECT FROM information_schema.tables 
  WHERE table_schema = 'public' 
  AND table_name = 'users'
);

-- List all tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- List all views
SELECT table_name 
FROM information_schema.views 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- List all enums
SELECT typname 
FROM pg_type 
WHERE typtype = 'e' 
ORDER BY typname;
```

## Rollback

To rollback migrations, drop tables in reverse order:

```sql
-- WARNING: This will delete all data!

-- Drop views first
DROP VIEW IF EXISTS weekly_adherence CASCADE;
DROP VIEW IF EXISTS user_current_streaks CASCADE;
DROP VIEW IF EXISTS family_daily_scores CASCADE;
DROP VIEW IF EXISTS active_routine_items CASCADE;

-- Drop tables in reverse dependency order
DROP TABLE IF EXISTS system_events CASCADE;
DROP TABLE IF EXISTS conversation_sessions CASCADE;
DROP TABLE IF EXISTS telegram_messages CASCADE;
DROP TABLE IF EXISTS telegram_users CASCADE;
DROP TABLE IF EXISTS reward_unlocks CASCADE;
DROP TABLE IF EXISTS reward_rules CASCADE;
DROP TABLE IF EXISTS rewards CASCADE;
DROP TABLE IF EXISTS daily_snapshots CASCADE;
DROP TABLE IF EXISTS body_metrics CASCADE;
DROP TABLE IF EXISTS workout_logs CASCADE;
DROP TABLE IF EXISTS workout_exercises CASCADE;
DROP TABLE IF EXISTS exercises CASCADE;
DROP TABLE IF EXISTS workout_sessions CASCADE;
DROP TABLE IF EXISTS workout_plans CASCADE;
DROP TABLE IF EXISTS habit_streaks CASCADE;
DROP TABLE IF EXISTS habit_logs CASCADE;
DROP TABLE IF EXISTS habits CASCADE;
DROP TABLE IF EXISTS routine_completions CASCADE;
DROP TABLE IF EXISTS routine_items CASCADE;
DROP TABLE IF EXISTS routine_cards CASCADE;
DROP TABLE IF EXISTS routine_versions CASCADE;
DROP TABLE IF EXISTS routines CASCADE;
DROP TABLE IF EXISTS family_memberships CASCADE;
DROP TABLE IF EXISTS families CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Drop enums
DROP TYPE IF EXISTS event_type CASCADE;
DROP TYPE IF EXISTS workout_goal CASCADE;
DROP TYPE IF EXISTS habit_type CASCADE;
DROP TYPE IF EXISTS routine_item_type CASCADE;
DROP TYPE IF EXISTS moment_of_day CASCADE;

-- Drop functions
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;
```

## Schema Documentation

Full schema documentation: `database/schema/DATABASE_SCHEMA.md`

## Notes

- All timestamps are stored in UTC
- Display times should be converted to user's timezone (default: America/Chicago)
- All tables use UUID primary keys
- Foreign keys use CASCADE delete where appropriate
- Indexes are created for common query patterns
- Views simplify complex queries

---

**Last Updated:** January 10, 2026
