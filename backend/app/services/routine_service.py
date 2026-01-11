"""
Routine Service

Business logic for routine operations.

This service handles:
- Creating routines
- Managing routine versions
- Querying routines
- Soft deleting routines
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Routine, RoutineVersion
from app.schemas import RoutineCreate, RoutineUpdate


class RoutineService:
    """
    Service for routine-related operations.
    
    Example:
    ```python
    service = RoutineService(db)
    routine = await service.create_routine(
        user_id=user.id,
        routine_data=RoutineCreate(name="Morning Routine")
    )
    ```
    """
    
    def __init__(self, db: AsyncSession):
        """Initialize service with database session."""
        self.db = db
    
    async def create_routine(
        self,
        user_id: UUID,
        routine_data: RoutineCreate
    ) -> Routine:
        """
        Create a new routine.
        
        Args:
            user_id: User UUID
            routine_data: Routine creation data
            
        Returns:
            Created routine
        """
        routine = Routine(
            user_id=user_id,
            **routine_data.model_dump()
        )
        self.db.add(routine)
        await self.db.flush()
        await self.db.refresh(routine)
        return routine
    
    async def get_routine_by_id(
        self,
        routine_id: UUID
    ) -> Optional[Routine]:
        """
        Get routine by ID.
        
        Args:
            routine_id: Routine UUID
            
        Returns:
            Routine if found, None otherwise
        """
        stmt = select(Routine).where(Routine.id == routine_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_user_routines(
        self,
        user_id: UUID,
        include_deleted: bool = False
    ) -> List[Routine]:
        """
        Get all routines for a user.
        
        Args:
            user_id: User UUID
            include_deleted: Not used (routines don't support soft delete)
            
        Returns:
            List of routines
        """
        stmt = select(Routine).where(Routine.user_id == user_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def update_routine(
        self,
        routine_id: UUID,
        routine_data: RoutineUpdate
    ) -> Optional[Routine]:
        """
        Update a routine.
        
        Args:
            routine_id: Routine UUID
            routine_data: Fields to update
            
        Returns:
            Updated routine if found, None otherwise
        """
        routine = await self.get_routine_by_id(routine_id)
        if not routine:
            return None
        
        # Update only provided fields
        for field, value in routine_data.model_dump(exclude_unset=True).items():
            setattr(routine, field, value)
        
        await self.db.flush()
        await self.db.refresh(routine)
        return routine
    
    async def delete_routine(
        self,
        routine_id: UUID
    ) -> bool:
        """
        Delete a routine (hard delete).
        
        Note: Routines don't support soft delete.
        This permanently removes the routine from the database.
        
        Args:
            routine_id: Routine UUID
            
        Returns:
            True if deleted, False if not found
        """
        routine = await self.get_routine_by_id(routine_id)
        if not routine:
            return False
        
        self.db.delete(routine)
        await self.db.flush()
        return True
