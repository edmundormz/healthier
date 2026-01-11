"""
Habit Pydantic Schemas

Schemas for habit-related API requests and responses.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


# =============================================================================
# Habit Schemas
# =============================================================================

class HabitBase(BaseModel):
    """Base habit schema."""
    name: str = Field(..., min_length=1, max_length=255)
    type: str = Field(default="boolean", pattern="^(boolean|numeric)$")
    target_value: Optional[Decimal] = None
    unit: Optional[str] = None
    active: bool = Field(default=True)


class HabitCreate(HabitBase):
    """Create habit request."""
    pass


class HabitUpdate(BaseModel):
    """Update habit request."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    target_value: Optional[Decimal] = None
    unit: Optional[str] = None
    active: Optional[bool] = None


class HabitResponse(HabitBase):
    """Habit response."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# Habit Log Schemas
# =============================================================================

class HabitLogBase(BaseModel):
    """Base habit log schema."""
    log_date: date = Field(default_factory=date.today)
    completed: bool = Field(default=False)
    value: Optional[Decimal] = None
    notes: Optional[str] = None


class HabitLogCreate(HabitLogBase):
    """Create habit log request."""
    habit_id: UUID


class HabitLogUpdate(BaseModel):
    """Update habit log request."""
    completed: Optional[bool] = None
    value: Optional[Decimal] = None
    notes: Optional[str] = None


class HabitLogResponse(HabitLogBase):
    """Habit log response."""
    id: UUID
    habit_id: UUID
    user_id: UUID
    logged_at: datetime
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# Habit Streak Schemas
# =============================================================================

class HabitStreakResponse(BaseModel):
    """Habit streak response."""
    id: UUID
    habit_id: UUID
    user_id: UUID
    current_streak: int
    longest_streak: int
    last_completed_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
