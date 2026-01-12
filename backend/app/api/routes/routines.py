"""
Routines API Routes

REST endpoints for routine management.

This module handles:
- Creating routines
- Getting routine information
- Updating routines
- Soft deleting routines
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models import User
from app.services.routine_service import RoutineService
from app.schemas import (
    RoutineCreate,
    RoutineUpdate,
    RoutineResponse,
)

router = APIRouter(prefix="/routines", tags=["routines"])


@router.post(
    "/",
    response_model=RoutineResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new routine",
    description="Creates a new routine for the specified user."
)
async def create_routine(
    routine_data: RoutineCreate = ...,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> RoutineResponse:
    """
    Create a new routine for the current user.
    
    Args:
        routine_data: Routine creation data
        current_user: Authenticated user (from Supabase JWT token)
        db: Database session
        
    Returns:
        Created routine
        
    Example:
    ```bash
    POST /api/routines/
    Authorization: Bearer <supabase_token>
    {
        "name": "Morning Routine",
        "description": "Daily morning protocol"
    }
    ```
    """
    # Create routine for current user
    service = RoutineService(db)
    routine = await service.create_routine(current_user.id, routine_data)
    await db.commit()
    
    return RoutineResponse.model_validate(routine)


@router.get(
    "/",
    response_model=List[RoutineResponse],
    summary="List routines",
    description="Returns routines for a specific user."
)
async def list_routines(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> List[RoutineResponse]:
    """
    Get all routines for the current user.
    
    Args:
        current_user: Authenticated user (from Supabase JWT token)
        db: Database session
        
    Returns:
        List of routines for the current user
        
    Example:
    ```bash
    GET /api/routines/
    Authorization: Bearer <supabase_token>
    ```
    """
    service = RoutineService(db)
    routines = await service.get_user_routines(current_user.id, include_deleted=False)
    return [RoutineResponse.model_validate(routine) for routine in routines]


@router.get(
    "/{routine_id}",
    response_model=RoutineResponse,
    summary="Get routine by ID",
    description="Returns a specific routine by its UUID."
)
async def get_routine(
    routine_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> RoutineResponse:
    """
    Get a routine by ID (only if owned by current user).
    
    Args:
        routine_id: Routine UUID
        current_user: Authenticated user (from Supabase JWT token)
        db: Database session
        
    Returns:
        Routine data
        
    Raises:
        HTTPException 404: If routine not found or not owned by user
        
    Example:
    ```bash
    GET /api/routines/550e8400-e29b-41d4-a716-446655440000
    Authorization: Bearer <supabase_token>
    ```
    """
    service = RoutineService(db)
    routine = await service.get_routine_by_id(routine_id)
    
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Routine with id {routine_id} not found"
        )
    
    # Verify routine belongs to current user
    if routine.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this routine"
        )
    
    return RoutineResponse.model_validate(routine)


@router.put(
    "/{routine_id}",
    response_model=RoutineResponse,
    summary="Update routine",
    description="Updates routine information. Only provided fields are updated."
)
async def update_routine(
    routine_id: UUID,
    routine_data: RoutineUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> RoutineResponse:
    """
    Update a routine (only if owned by current user).
    
    Args:
        routine_id: Routine UUID
        routine_data: Fields to update (all optional)
        current_user: Authenticated user (from Supabase JWT token)
        db: Database session
        
    Returns:
        Updated routine
        
    Raises:
        HTTPException 404: If routine not found
        HTTPException 403: If routine not owned by user
        
    Example:
    ```bash
    PUT /api/routines/550e8400-e29b-41d4-a716-446655440000
    Authorization: Bearer <supabase_token>
    {
        "name": "Updated Morning Routine",
        "description": "New description"
    }
    ```
    """
    service = RoutineService(db)
    
    # Check if routine exists and belongs to user
    routine = await service.get_routine_by_id(routine_id)
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Routine with id {routine_id} not found"
        )
    
    # Verify routine belongs to current user
    if routine.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this routine"
        )
    
    # Update routine
    updated_routine = await service.update_routine(routine_id, routine_data)
    await db.commit()
    
    return RoutineResponse.model_validate(updated_routine)


@router.delete(
    "/{routine_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete routine",
    description="Soft deletes a routine. Routine data is preserved but marked as deleted."
)
async def delete_routine(
    routine_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete a routine (only if owned by current user).
    
    Args:
        routine_id: Routine UUID
        current_user: Authenticated user (from Supabase JWT token)
        db: Database session
        
    Raises:
        HTTPException 404: If routine not found
        HTTPException 403: If routine not owned by user
        
    Example:
    ```bash
    DELETE /api/routines/550e8400-e29b-41d4-a716-446655440000
    Authorization: Bearer <supabase_token>
    ```
    """
    service = RoutineService(db)
    
    # Check if routine exists and belongs to user
    routine = await service.get_routine_by_id(routine_id)
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Routine with id {routine_id} not found"
        )
    
    # Verify routine belongs to current user
    if routine.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this routine"
        )
    
    success = await service.delete_routine(routine_id)
    await db.commit()
