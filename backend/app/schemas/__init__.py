"""
Pydantic Schemas

These schemas define the structure of API requests and responses.

Usage:
```python
from app.schemas import UserCreate, UserResponse, HabitCreate
```
"""

from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserBrief,
    FamilyBase,
    FamilyCreate,
    FamilyUpdate,
    FamilyResponse,
    FamilyMembershipBase,
    FamilyMembershipCreate,
    FamilyMembershipUpdate,
    FamilyMembershipResponse,
    FamilyMembershipWithUser,
)

from app.schemas.routine import (
    RoutineBase,
    RoutineCreate,
    RoutineUpdate,
    RoutineResponse,
    RoutineVersionBase,
    RoutineVersionCreate,
    RoutineVersionResponse,
    RoutineItemBase,
    RoutineItemCreate,
    RoutineItemUpdate,
    RoutineItemResponse,
    RoutineCompletionBase,
    RoutineCompletionCreate,
    RoutineCompletionResponse,
)

from app.schemas.habit import (
    HabitBase,
    HabitCreate,
    HabitUpdate,
    HabitResponse,
    HabitLogBase,
    HabitLogCreate,
    HabitLogUpdate,
    HabitLogResponse,
    HabitStreakResponse,
)

__all__ = [
    # Users
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserBrief",
    # Families
    "FamilyBase",
    "FamilyCreate",
    "FamilyUpdate",
    "FamilyResponse",
    # Family Memberships
    "FamilyMembershipBase",
    "FamilyMembershipCreate",
    "FamilyMembershipUpdate",
    "FamilyMembershipResponse",
    "FamilyMembershipWithUser",
    # Routines
    "RoutineBase",
    "RoutineCreate",
    "RoutineUpdate",
    "RoutineResponse",
    "RoutineVersionBase",
    "RoutineVersionCreate",
    "RoutineVersionResponse",
    "RoutineItemBase",
    "RoutineItemCreate",
    "RoutineItemUpdate",
    "RoutineItemResponse",
    "RoutineCompletionBase",
    "RoutineCompletionCreate",
    "RoutineCompletionResponse",
    # Habits
    "HabitBase",
    "HabitCreate",
    "HabitUpdate",
    "HabitResponse",
    "HabitLogBase",
    "HabitLogCreate",
    "HabitLogUpdate",
    "HabitLogResponse",
    "HabitStreakResponse",
]
