"""
Authentication Schemas

Schemas for authentication endpoints (login, signup, token refresh).

These schemas handle:
- User registration (signup)
- User login (email + password)
- Token responses (access token)
- Password validation rules
"""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


# =============================================================================
# Request Schemas
# =============================================================================

class UserSignup(BaseModel):
    """
    Schema for user registration (signup).
    
    This is similar to UserCreate but includes password.
    Password is validated for strength.
    
    Example:
    ```json
    {
        "email": "candy@example.com",
        "password": "SecurePassword123!",
        "full_name": "Candy Hernández",
        "language": "es"
    }
    ```
    """
    
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="User password (min 8 characters)"
    )
    full_name: str = Field(..., min_length=1, max_length=255, description="User's full name")
    timezone: str = Field(default="America/Chicago", description="User's timezone")
    language: str = Field(default="es", pattern="^(es|en)$", description="Preferred language")
    notification_enabled: bool = Field(default=True, description="Enable notifications")
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """
        Validate password strength.
        
        Requirements:
        - At least 8 characters
        - Should contain letters and numbers (recommended)
        
        Note: We keep validation simple for MVP.
        Can add more complex rules later (uppercase, special chars, etc.)
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class UserLogin(BaseModel):
    """
    Schema for user login.
    
    Example:
    ```json
    {
        "email": "candy@example.com",
        "password": "SecurePassword123!"
    }
    ```
    """
    
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User password")


# =============================================================================
# Response Schemas
# =============================================================================

class TokenResponse(BaseModel):
    """
    Schema for authentication token response.
    
    Returns the access token that clients use for authenticated requests.
    
    Example:
    ```json
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer",
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "candy@example.com"
    }
    ```
    """
    
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type (always 'bearer')")
    user_id: UUID = Field(..., description="Authenticated user's ID")
    email: EmailStr = Field(..., description="Authenticated user's email")


class UserInfo(BaseModel):
    """
    Schema for authenticated user info.
    
    Used when returning current user information.
    
    Example:
    ```json
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "candy@example.com",
        "full_name": "Candy Hernández",
        "language": "es"
    }
    ```
    """
    
    id: UUID
    email: EmailStr
    full_name: str
    language: str
    timezone: str
    notification_enabled: bool
