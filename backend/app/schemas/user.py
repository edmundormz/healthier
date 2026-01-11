"""
User Pydantic Schemas

These schemas define the structure of data for API requests and responses.

Why separate from SQLAlchemy models?
- SQLAlchemy models = Database structure
- Pydantic schemas = API structure
- They serve different purposes and can differ

Pydantic provides:
- Automatic validation
- Type checking
- JSON serialization
- OpenAPI documentation

See: https://docs.pydantic.dev/latest/
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict


# =============================================================================
# Base Schemas
# =============================================================================

class UserBase(BaseModel):
    """Base schema with common user fields."""
    
    email: EmailStr = Field(..., description="User's email address")
    full_name: str = Field(..., min_length=1, max_length=255, description="User's full name")
    timezone: str = Field(default="America/Chicago", description="User's timezone")
    language: str = Field(default="es", pattern="^(es|en)$", description="Preferred language")
    notification_enabled: bool = Field(default=True, description="Enable notifications")


# =============================================================================
# Request Schemas (for creating/updating)
# =============================================================================

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    
    Example:
    ```json
    {
        "email": "candy@example.com",
        "full_name": "Candy Hernández",
        "language": "es"
    }
    ```
    """
    pass


class UserUpdate(BaseModel):
    """
    Schema for updating a user.
    
    All fields are optional - only update what's provided.
    
    Example:
    ```json
    {
        "full_name": "Candy Hernández-Ramirez",
        "notification_enabled": false
    }
    ```
    """
    
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    timezone: Optional[str] = None
    language: Optional[str] = Field(None, pattern="^(es|en)$")
    notification_enabled: Optional[bool] = None


# =============================================================================
# Response Schemas
# =============================================================================

class UserResponse(UserBase):
    """
    Schema for user response (includes database fields).
    
    This is what the API returns when querying users.
    
    Example:
    ```json
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "candy@example.com",
        "full_name": "Candy Hernández",
        "timezone": "America/Chicago",
        "language": "es",
        "notification_enabled": true,
        "last_active_at": "2026-01-10T12:30:00Z",
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-10T12:30:00Z",
        "deleted_at": null
    }
    ```
    """
    
    id: UUID
    last_active_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
    # Pydantic v2 configuration
    # This allows creating Pydantic models from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)


class UserBrief(BaseModel):
    """
    Brief user info (for nested responses).
    
    Used when including user info in other responses,
    without all the details.
    
    Example:
    ```json
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "candy@example.com",
        "full_name": "Candy Hernández"
    }
    ```
    """
    
    id: UUID
    email: EmailStr
    full_name: str
    
    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# Family Schemas
# =============================================================================

class FamilyBase(BaseModel):
    """Base schema with common family fields."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Family name")


class FamilyCreate(FamilyBase):
    """
    Schema for creating a new family.
    
    Example:
    ```json
    {
        "name": "Family CH"
    }
    ```
    """
    pass


class FamilyUpdate(BaseModel):
    """Schema for updating a family."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)


class FamilyResponse(FamilyBase):
    """
    Schema for family response.
    
    Example:
    ```json
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Family CH",
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-10T12:30:00Z"
    }
    ```
    """
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# Family Membership Schemas
# =============================================================================

class FamilyMembershipBase(BaseModel):
    """Base schema with common membership fields."""
    
    role: str = Field(default="member", pattern="^(admin|member)$", description="User role in family")


class FamilyMembershipCreate(FamilyMembershipBase):
    """
    Schema for creating a family membership.
    
    Example:
    ```json
    {
        "family_id": "550e8400-e29b-41d4-a716-446655440000",
        "user_id": "650e8400-e29b-41d4-a716-446655440000",
        "role": "admin"
    }
    ```
    """
    
    family_id: UUID
    user_id: UUID


class FamilyMembershipUpdate(BaseModel):
    """Schema for updating a family membership."""
    
    role: Optional[str] = Field(None, pattern="^(admin|member)$")


class FamilyMembershipResponse(FamilyMembershipBase):
    """
    Schema for family membership response.
    
    Example:
    ```json
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "family_id": "550e8400-e29b-41d4-a716-446655440000",
        "user_id": "650e8400-e29b-41d4-a716-446655440000",
        "role": "admin",
        "joined_at": "2026-01-01T00:00:00Z",
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z"
    }
    ```
    """
    
    id: UUID
    family_id: UUID
    user_id: UUID
    joined_at: datetime
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class FamilyMembershipWithUser(FamilyMembershipResponse):
    """
    Family membership with nested user info.
    
    Useful for listing family members.
    
    Example:
    ```json
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "role": "admin",
        "joined_at": "2026-01-01T00:00:00Z",
        "user": {
            "id": "650e8400-e29b-41d4-a716-446655440000",
            "email": "candy@example.com",
            "full_name": "Candy Hernández"
        }
    }
    ```
    """
    
    user: UserBrief
