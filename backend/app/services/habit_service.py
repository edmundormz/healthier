"""
Habit Service

Business logic for habit operations.

This service handles:
- Creating habits
- Querying habits
- Updating habits
- Soft deleting habits
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Habit
from app.schemas import HabitCreate, HabitUpdate


class HabitService:
    """
    Service for habit-related operations.
    
    Example:
    ```python
    service = HabitService(db)
    habit = await service.create_habit(
        user_id=user.id,
        habit_data=HabitCreate(name="Walk 10k steps", type="numeric")
    )
    ```
    """
    
    def __init__(self, db: AsyncSession):
        """Initialize service with database session."""
        self.db = db
    
    async def create_habit(
        self,
        user_id: UUID,
        habit_data: HabitCreate
    ) -> Habit:
        """
        Create a new habit.
        
        Args:
            user_id: User UUID
            habit_data: Habit creation data
            
        Returns:
            Created habit
        """
        habit = Habit(
            user_id=user_id,
            **habit_data.model_dump()
        )
        self.db.add(habit)
        await self.db.flush()
        await self.db.refresh(habit)
        return habit
    
    async def get_habit_by_id(
        self,
        habit_id: UUID
    ) -> Optional[Habit]:
        """
        Get habit by ID.
        
        Args:
            habit_id: Habit UUID
            
        Returns:
            Habit if found, None otherwise
        """
        stmt = select(Habit).where(Habit.id == habit_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_user_habits(
        self,
        user_id: UUID,
        include_deleted: bool = False,
        active_only: bool = False
    ) -> List[Habit]:
        """
        Get all habits for a user.
        
        Args:
            user_id: User UUID
            include_deleted: Not used (habits don't support soft delete)
            active_only: Only return active habits
            
        Returns:
            List of habits
        """
        stmt = select(Habit).where(Habit.user_id == user_id)
        
        if active_only:
            stmt = stmt.where(Habit.active == True)
        
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def update_habit(
        self,
        habit_id: UUID,
        habit_data: HabitUpdate
    ) -> Optional[Habit]:
        """
        Update a habit.
        
        Args:
            habit_id: Habit UUID
            habit_data: Fields to update
            
        Returns:
            Updated habit if found, None otherwise
        """
        habit = await self.get_habit_by_id(habit_id)
        if not habit:
            return None
        
        # Update only provided fields
        for field, value in habit_data.model_dump(exclude_unset=True).items():
            setattr(habit, field, value)
        
        await self.db.flush()
        await self.db.refresh(habit)
        return habit
    
    async def delete_habit(
        self,
        habit_id: UUID
    ) -> bool:
        """
        Delete a habit (hard delete).
        
        Note: Habits don't support soft delete.
        This permanently removes the habit from the database.
        
        Args:
            habit_id: Habit UUID
            
        Returns:
            True if deleted, False if not found
        """
        habit = await self.get_habit_by_id(habit_id)
        if not habit:
            return False
        
        self.db.delete(habit)
        await self.db.flush()
        return True
