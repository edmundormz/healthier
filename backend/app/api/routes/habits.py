"""
Habits API Routes

REST endpoints for habit management.

This module handles:
- Creating habits
- Getting habit information
- Updating habits
- Soft deleting habits
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models import User
from app.services.habit_service import HabitService
from app.schemas import (
    HabitCreate,
    HabitUpdate,
    HabitResponse,
)

router = APIRouter(prefix="/habits", tags=["habits"])


@router.post(
    "/",
    response_model=HabitResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new habit",
    description="Creates a new habit for the specified user."
)
async def create_habit(
    habit_data: HabitCreate = ...,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> HabitResponse:
    """
    Create a new habit for the current user.
    
    Args:
        habit_data: Habit creation data
        current_user: Authenticated user (from Supabase JWT token)
        db: Database session
        
    Returns:
        Created habit
        
    Example:
    ```bash
    POST /api/habits/
    Authorization: Bearer <supabase_token>
    {
        "name": "Walk 10k steps",
        "type": "numeric",
        "target_value": 10000,
        "unit": "steps"
    }
    ```
    """
    # Create habit for current user
    service = HabitService(db)
    habit = await service.create_habit(current_user.id, habit_data)
    await db.commit()
    
    return HabitResponse.model_validate(habit)


@router.get(
    "/",
    response_model=List[HabitResponse],
    summary="List habits",
    description="Returns habits for a specific user."
)
async def list_habits(
    active_only: bool = Query(False, description="Only return active habits"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> List[HabitResponse]:
    """
    Get all habits for the current user.
    
    Args:
        active_only: Only return active habits
        current_user: Authenticated user (from Supabase JWT token)
        db: Database session
        
    Returns:
        List of habits for the current user
        
    Example:
    ```bash
    GET /api/habits/
    GET /api/habits/?active_only=true
    Authorization: Bearer <supabase_token>
    ```
    """
    service = HabitService(db)
    habits = await service.get_user_habits(current_user.id, include_deleted=False, active_only=active_only)
    return [HabitResponse.model_validate(habit) for habit in habits]


@router.get(
    "/{habit_id}",
    response_model=HabitResponse,
    summary="Get habit by ID",
    description="Returns a specific habit by its UUID."
)
async def get_habit(
    habit_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> HabitResponse:
    """
    Get a habit by ID (only if owned by current user).
    
    Args:
        habit_id: Habit UUID
        current_user: Authenticated user (from Supabase JWT token)
        db: Database session
        
    Returns:
        Habit data
        
    Raises:
        HTTPException 404: If habit not found or not owned by user
        
    Example:
    ```bash
    GET /api/habits/550e8400-e29b-41d4-a716-446655440000
    Authorization: Bearer <supabase_token>
    ```
    """
    service = HabitService(db)
    habit = await service.get_habit_by_id(habit_id)
    
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Habit with id {habit_id} not found"
        )
    
    # Verify habit belongs to current user
    if habit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this habit"
        )
    
    return HabitResponse.model_validate(habit)


@router.put(
    "/{habit_id}",
    response_model=HabitResponse,
    summary="Update habit",
    description="Updates habit information. Only provided fields are updated."
)
async def update_habit(
    habit_id: UUID,
    habit_data: HabitUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> HabitResponse:
    """
    Update a habit (only if owned by current user).
    
    Args:
        habit_id: Habit UUID
        habit_data: Fields to update (all optional)
        current_user: Authenticated user (from Supabase JWT token)
        db: Database session
        
    Returns:
        Updated habit
        
    Raises:
        HTTPException 404: If habit not found
        HTTPException 403: If habit not owned by user
        
    Example:
    ```bash
    PUT /api/habits/550e8400-e29b-41d4-a716-446655440000
    Authorization: Bearer <supabase_token>
    {
        "name": "Walk 12k steps",
        "target_value": 12000,
        "active": false
    }
    ```
    """
    service = HabitService(db)
    
    # Check if habit exists and belongs to user
    habit = await service.get_habit_by_id(habit_id)
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Habit with id {habit_id} not found"
        )
    
    # Verify habit belongs to current user
    if habit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this habit"
        )
    
    # Update habit
    updated_habit = await service.update_habit(habit_id, habit_data)
    await db.commit()
    
    return HabitResponse.model_validate(updated_habit)


@router.delete(
    "/{habit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete habit",
    description="Soft deletes a habit. Habit data is preserved but marked as deleted."
)
async def delete_habit(
    habit_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete a habit (only if owned by current user).
    
    Args:
        habit_id: Habit UUID
        current_user: Authenticated user (from Supabase JWT token)
        db: Database session
        
    Raises:
        HTTPException 404: If habit not found
        HTTPException 403: If habit not owned by user
        
    Example:
    ```bash
    DELETE /api/habits/550e8400-e29b-41d4-a716-446655440000
    Authorization: Bearer <supabase_token>
    ```
    """
    service = HabitService(db)
    
    # Check if habit exists and belongs to user
    habit = await service.get_habit_by_id(habit_id)
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Habit with id {habit_id} not found"
        )
    
    # Verify habit belongs to current user
    if habit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this habit"
        )
    
    success = await service.delete_habit(habit_id)
    await db.commit()
