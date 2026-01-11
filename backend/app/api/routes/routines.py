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

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.routine_service import RoutineService
from app.services import UserService
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
    user_id: UUID = Query(..., description="User UUID (owner of the routine)"),
    routine_data: RoutineCreate = ...,
    db: AsyncSession = Depends(get_db)
) -> RoutineResponse:
    """
    Create a new routine.
    
    Args:
        user_id: User UUID (owner of the routine)
        routine_data: Routine creation data
        db: Database session
        
    Returns:
        Created routine
        
    Raises:
        HTTPException 404: If user not found
        
    Example:
    ```bash
    POST /api/routines/?user_id=550e8400-e29b-41d4-a716-446655440000
    {
        "name": "Morning Routine",
        "description": "Daily morning protocol"
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
    
    # Create routine
    service = RoutineService(db)
    routine = await service.create_routine(user_id, routine_data)
    await db.commit()
    
    return RoutineResponse.model_validate(routine)


@router.get(
    "/",
    response_model=List[RoutineResponse],
    summary="List routines",
    description="Returns routines for a specific user."
)
async def list_routines(
    user_id: UUID = Query(..., description="User UUID"),
    include_deleted: bool = Query(False, description="Include soft-deleted routines"),
    db: AsyncSession = Depends(get_db)
) -> List[RoutineResponse]:
    """
    Get all routines for a user.
    
    Args:
        user_id: User UUID
        include_deleted: Include soft-deleted routines
        db: Database session
        
    Returns:
        List of routines
        
    Example:
    ```bash
    GET /api/routines/?user_id=550e8400-e29b-41d4-a716-446655440000
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
    
    service = RoutineService(db)
    routines = await service.get_user_routines(user_id, include_deleted)
    return [RoutineResponse.model_validate(routine) for routine in routines]


@router.get(
    "/{routine_id}",
    response_model=RoutineResponse,
    summary="Get routine by ID",
    description="Returns a specific routine by its UUID."
)
async def get_routine(
    routine_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> RoutineResponse:
    """
    Get a routine by ID.
    
    Args:
        routine_id: Routine UUID
        db: Database session
        
    Returns:
        Routine data
        
    Raises:
        HTTPException 404: If routine not found
        
    Example:
    ```bash
    GET /api/routines/550e8400-e29b-41d4-a716-446655440000
    ```
    """
    service = RoutineService(db)
    routine = await service.get_routine_by_id(routine_id)
    
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Routine with id {routine_id} not found"
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
    db: AsyncSession = Depends(get_db)
) -> RoutineResponse:
    """
    Update a routine.
    
    Args:
        routine_id: Routine UUID
        routine_data: Fields to update (all optional)
        db: Database session
        
    Returns:
        Updated routine
        
    Raises:
        HTTPException 404: If routine not found
        
    Example:
    ```bash
    PUT /api/routines/550e8400-e29b-41d4-a716-446655440000
    {
        "name": "Updated Morning Routine",
        "description": "New description"
    }
    ```
    """
    service = RoutineService(db)
    
    # Check if routine exists
    routine = await service.get_routine_by_id(routine_id)
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Routine with id {routine_id} not found"
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
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Soft delete a routine.
    
    Args:
        routine_id: Routine UUID
        db: Database session
        
    Raises:
        HTTPException 404: If routine not found
        
    Example:
    ```bash
    DELETE /api/routines/550e8400-e29b-41d4-a716-446655440000
    ```
    """
    service = RoutineService(db)
    success = await service.delete_routine(routine_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Routine with id {routine_id} not found"
        )
    
    await db.commit()
