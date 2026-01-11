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
from app.services.habit_service import HabitService
from app.services import UserService
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
    user_id: UUID = Query(..., description="User UUID (owner of the habit)"),
    habit_data: HabitCreate = ...,
    db: AsyncSession = Depends(get_db)
) -> HabitResponse:
    """
    Create a new habit.
    
    Args:
        user_id: User UUID (owner of the habit)
        habit_data: Habit creation data
        db: Database session
        
    Returns:
        Created habit
        
    Raises:
        HTTPException 404: If user not found
        
    Example:
    ```bash
    POST /api/habits/?user_id=550e8400-e29b-41d4-a716-446655440000
    {
        "name": "Walk 10k steps",
        "type": "numeric",
        "target_value": 10000,
        "unit": "steps"
    }
    ```
    """
    # Verify user exists
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # Create habit
    service = HabitService(db)
    habit = await service.create_habit(user_id, habit_data)
    await db.commit()
    
    return HabitResponse.model_validate(habit)


@router.get(
    "/",
    response_model=List[HabitResponse],
    summary="List habits",
    description="Returns habits for a specific user."
)
async def list_habits(
    user_id: UUID = Query(..., description="User UUID"),
    include_deleted: bool = Query(False, description="Include soft-deleted habits"),
    active_only: bool = Query(False, description="Only return active habits"),
    db: AsyncSession = Depends(get_db)
) -> List[HabitResponse]:
    """
    Get all habits for a user.
    
    Args:
        user_id: User UUID
        include_deleted: Include soft-deleted habits
        active_only: Only return active habits
        db: Database session
        
    Returns:
        List of habits
        
    Example:
    ```bash
    GET /api/habits/?user_id=550e8400-e29b-41d4-a716-446655440000
    GET /api/habits/?user_id=550e8400-e29b-41d4-a716-446655440000&active_only=true
    ```
    """
    # Verify user exists
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    service = HabitService(db)
    habits = await service.get_user_habits(user_id, include_deleted, active_only)
    return [HabitResponse.model_validate(habit) for habit in habits]


@router.get(
    "/{habit_id}",
    response_model=HabitResponse,
    summary="Get habit by ID",
    description="Returns a specific habit by its UUID."
)
async def get_habit(
    habit_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> HabitResponse:
    """
    Get a habit by ID.
    
    Args:
        habit_id: Habit UUID
        db: Database session
        
    Returns:
        Habit data
        
    Raises:
        HTTPException 404: If habit not found
        
    Example:
    ```bash
    GET /api/habits/550e8400-e29b-41d4-a716-446655440000
    ```
    """
    service = HabitService(db)
    habit = await service.get_habit_by_id(habit_id)
    
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Habit with id {habit_id} not found"
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
    db: AsyncSession = Depends(get_db)
) -> HabitResponse:
    """
    Update a habit.
    
    Args:
        habit_id: Habit UUID
        habit_data: Fields to update (all optional)
        db: Database session
        
    Returns:
        Updated habit
        
    Raises:
        HTTPException 404: If habit not found
        
    Example:
    ```bash
    PUT /api/habits/550e8400-e29b-41d4-a716-446655440000
    {
        "name": "Walk 12k steps",
        "target_value": 12000,
        "active": false
    }
    ```
    """
    service = HabitService(db)
    
    # Check if habit exists
    habit = await service.get_habit_by_id(habit_id)
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Habit with id {habit_id} not found"
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
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Soft delete a habit.
    
    Args:
        habit_id: Habit UUID
        db: Database session
        
    Raises:
        HTTPException 404: If habit not found
        
    Example:
    ```bash
    DELETE /api/habits/550e8400-e29b-41d4-a716-446655440000
    ```
    """
    service = HabitService(db)
    success = await service.delete_habit(habit_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Habit with id {habit_id} not found"
        )
    
    await db.commit()
