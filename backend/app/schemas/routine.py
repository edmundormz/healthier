"""
Routine Pydantic Schemas

Schemas for routine-related API requests and responses.
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


# =============================================================================
# Routine Schemas
# =============================================================================

class RoutineBase(BaseModel):
    """Base routine schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class RoutineCreate(RoutineBase):
    """Create routine request."""
    pass


class RoutineUpdate(BaseModel):
    """Update routine request."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


class RoutineResponse(RoutineBase):
    """Routine response."""
    id: UUID
    user_id: UUID
    active_version_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# Routine Version Schemas
# =============================================================================

class RoutineVersionBase(BaseModel):
    """Base routine version schema."""
    start_date: date
    end_date: Optional[date] = None
    notes: Optional[str] = None


class RoutineVersionCreate(RoutineVersionBase):
    """Create routine version request."""
    routine_id: UUID


class RoutineVersionResponse(RoutineVersionBase):
    """Routine version response."""
    id: UUID
    routine_id: UUID
    version_number: int
    created_by: Optional[UUID] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# Routine Item Schemas
# =============================================================================

class RoutineItemBase(BaseModel):
    """Base routine item schema."""
    type: str = Field(..., pattern="^(medication|supplement|skincare|hair_care|habit)$")
    name: str = Field(..., min_length=1, max_length=255)
    dosage: Optional[str] = None
    instructions: Optional[str] = None
    frequency: str = Field(default="daily")
    expires_at: Optional[date] = None
    duration_days: Optional[int] = None
    sort_order: int = Field(default=0)


class RoutineItemCreate(RoutineItemBase):
    """Create routine item request."""
    routine_card_id: UUID
    next_item_id: Optional[UUID] = None


class RoutineItemUpdate(BaseModel):
    """Update routine item request."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    dosage: Optional[str] = None
    instructions: Optional[str] = None
    frequency: Optional[str] = None
    expires_at: Optional[date] = None
    duration_days: Optional[int] = None
    sort_order: Optional[int] = None


class RoutineItemResponse(RoutineItemBase):
    """Routine item response."""
    id: UUID
    routine_card_id: UUID
    next_item_id: Optional[UUID] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# Routine Completion Schemas
# =============================================================================

class RoutineCompletionBase(BaseModel):
    """Base routine completion schema."""
    completion_date: date = Field(default_factory=date.today)
    notes: Optional[str] = None
    skipped: bool = Field(default=False)
    skip_reason: Optional[str] = None


class RoutineCompletionCreate(RoutineCompletionBase):
    """Create routine completion request."""
    routine_item_id: UUID


class RoutineCompletionResponse(RoutineCompletionBase):
    """Routine completion response."""
    id: UUID
    user_id: UUID
    routine_item_id: UUID
    completed_at: datetime
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
