"""
Database Models

This module exports all SQLAlchemy models for easy importing.

Usage:
```python
from app.models import User, Family, Routine, Habit
```

Why centralized imports?
- Convenient: Import from one place
- Clear: See all available models at a glance
- Migration support: Alembic can discover all models
- Relationship resolution: SQLAlchemy needs all models loaded

See: https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html
"""

# Base and mixins
from app.models.base import (
    Base,
    BaseModel,
    BaseModelWithSoftDelete,
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
)

# User models
from app.models.user import (
    User,
    Family,
    FamilyMembership,
)

# Routine models
from app.models.routine import (
    Routine,
    RoutineVersion,
    RoutineCard,
    RoutineItem,
    RoutineCompletion,
    MomentOfDay,
    RoutineItemType,
)

# Habit models
from app.models.habit import (
    Habit,
    HabitLog,
    HabitStreak,
    HabitType,
)

# Export all models
__all__ = [
    # Base
    "Base",
    "BaseModel",
    "BaseModelWithSoftDelete",
    "UUIDMixin",
    "TimestampMixin",
    "SoftDeleteMixin",
    # Users
    "User",
    "Family",
    "FamilyMembership",
    # Routines
    "Routine",
    "RoutineVersion",
    "RoutineCard",
    "RoutineItem",
    "RoutineCompletion",
    "MomentOfDay",
    "RoutineItemType",
    # Habits
    "Habit",
    "HabitLog",
    "HabitStreak",
    "HabitType",
]
