"""
Users API Routes

REST endpoints for user management.

This module handles:
- Creating users
- Getting user information
- Updating users
- Soft deleting users
- Family management

Pattern:
    Request → Pydantic Schema → Service → Database → Response Schema

See: https://fastapi.tiangolo.com/tutorial/bigger-applications/
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services import UserService, FamilyService
from app.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    FamilyCreate,
    FamilyResponse,
    FamilyMembershipCreate,
    FamilyMembershipResponse,
)

# Create router with prefix and tags
# Prefix: All routes will start with /users
# Tags: Groups endpoints in OpenAPI docs
router = APIRouter(prefix="/users", tags=["users"])


# =============================================================================
# User Endpoints
# =============================================================================

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Creates a new user account. Email must be unique."
)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Create a new user.
    
    This endpoint:
    1. Validates the request data (via Pydantic)
    2. Checks if email already exists
    3. Creates the user in the database
    4. Returns the created user
    
    Args:
        user_data: User creation data (email, full_name, etc.)
        db: Database session (injected by FastAPI)
        
    Returns:
        Created user with all fields
        
    Raises:
        HTTPException 400: If email already exists
        HTTPException 500: If database error occurs
        
    Example:
    ```bash
    POST /api/users/
    {
        "email": "candy@example.com",
        "full_name": "Candy Hernández",
        "language": "es"
    }
    ```
    """
    service = UserService(db)
    
    # Check if email already exists
    existing_user = await service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user_data.email} already exists"
        )
    
    # Create user
    user = await service.create_user(user_data)
    await db.commit()  # Commit transaction
    
    return UserResponse.model_validate(user)


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="List all users",
    description="Returns a list of all active users."
)
async def list_users(
    include_deleted: bool = False,
    db: AsyncSession = Depends(get_db)
) -> List[UserResponse]:
    """
    Get all users.
    
    Args:
        include_deleted: Include soft-deleted users (default: False)
        db: Database session
        
    Returns:
        List of users
        
    Example:
    ```bash
    GET /api/users/
    GET /api/users/?include_deleted=true
    ```
    """
    service = UserService(db)
    users = await service.get_all_users(include_deleted=include_deleted)
    return [UserResponse.model_validate(user) for user in users]


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Returns a specific user by their UUID."
)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Get a user by ID.
    
    Args:
        user_id: User UUID
        db: Database session
        
    Returns:
        User data
        
    Raises:
        HTTPException 404: If user not found
        
    Example:
    ```bash
    GET /api/users/550e8400-e29b-41d4-a716-446655440000
    ```
    """
    service = UserService(db)
    user = await service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    return UserResponse.model_validate(user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description="Updates user information. Only provided fields are updated."
)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Update a user.
    
    This endpoint uses Pydantic's `exclude_unset=True` to only update
    fields that are provided in the request.
    
    Args:
        user_id: User UUID
        user_data: Fields to update (all optional)
        db: Database session
        
    Returns:
        Updated user
        
    Raises:
        HTTPException 404: If user not found
        
    Example:
    ```bash
    PUT /api/users/550e8400-e29b-41d4-a716-446655440000
    {
        "full_name": "Candy Hernández-Ramirez",
        "notification_enabled": false
    }
    ```
    """
    service = UserService(db)
    
    # Check if user exists
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # Update user
    updated_user = await service.update_user(user_id, user_data)
    await db.commit()
    
    return UserResponse.model_validate(updated_user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Soft deletes a user. User data is preserved but marked as deleted."
)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Soft delete a user.
    
    This doesn't actually delete the record from the database.
    Instead, it sets the `deleted_at` timestamp, which hides
    the user from normal queries.
    
    Args:
        user_id: User UUID
        db: Database session
        
    Raises:
        HTTPException 404: If user not found
        
    Example:
    ```bash
    DELETE /api/users/550e8400-e29b-41d4-a716-446655440000
    ```
    """
    service = UserService(db)
    success = await service.soft_delete_user(user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    await db.commit()


@router.post(
    "/{user_id}/restore",
    response_model=UserResponse,
    summary="Restore deleted user",
    description="Restores a soft-deleted user."
)
async def restore_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Restore a soft-deleted user.
    
    Args:
        user_id: User UUID
        db: Database session
        
    Returns:
        Restored user
        
    Raises:
        HTTPException 404: If user not found or not deleted
    """
    service = UserService(db)
    success = await service.restore_user(user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found or not deleted"
        )
    
    await db.commit()
    
    # Get restored user
    user = await service.get_user_by_id(user_id)
    return UserResponse.model_validate(user)


# =============================================================================
# Family Endpoints
# =============================================================================

@router.post(
    "/{user_id}/families",
    response_model=FamilyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a family",
    description="Creates a new family and adds the user as an admin member."
)
async def create_family(
    user_id: UUID,
    family_data: FamilyCreate,
    db: AsyncSession = Depends(get_db)
) -> FamilyResponse:
    """
    Create a family and add the user as admin.
    
    Args:
        user_id: User UUID (will be added as admin)
        family_data: Family creation data
        db: Database session
        
    Returns:
        Created family
        
    Raises:
        HTTPException 404: If user not found
    """
    # Verify user exists
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # Create family
    family_service = FamilyService(db)
    family = await family_service.create_family(family_data)
    
    # Add user as admin
    await family_service.add_member(
        family_id=family.id,
        user_id=user_id,
        role="admin"
    )
    
    await db.commit()
    return FamilyResponse.model_validate(family)


@router.get(
    "/{user_id}/families",
    response_model=List[FamilyResponse],
    summary="Get user's families",
    description="Returns all families the user belongs to."
)
async def get_user_families(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> List[FamilyResponse]:
    """
    Get all families a user belongs to.
    
    Args:
        user_id: User UUID
        db: Database session
        
    Returns:
        List of families
    """
    # Verify user exists
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    family_service = FamilyService(db)
    families = await family_service.get_user_families(user_id)
    return [FamilyResponse.model_validate(family) for family in families]
