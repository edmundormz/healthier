"""
User Service

Business logic for user operations.

Why Services?
- Separation of concerns: Keep API routes thin
- Reusability: Same logic used by API, CLI, background tasks
- Testability: Easy to test without HTTP layer
- Transaction management: Complex operations in one transaction

Pattern:
    API Route → Service → Database (via SQLAlchemy)

See: Repository pattern
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Family, FamilyMembership
from app.schemas import (
    UserCreate,
    UserUpdate,
    FamilyCreate,
    FamilyMembershipCreate,
)


class UserService:
    """
    Service for user-related operations.
    
    This class encapsulates all user business logic:
    - Creating users
    - Updating users
    - Querying users
    - Soft deleting users
    
    Example:
    ```python
    async with AsyncSessionLocal() as session:
        service = UserService(session)
        user = await service.create_user(
            UserCreate(
                email="candy@example.com",
                full_name="Candy Hernández"
            )
        )
    ```
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy async session
        """
        self.db = db
    
    async def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user.
        
        Args:
            user_data: User creation data
            
        Returns:
            Created user
            
        Example:
        ```python
        user = await service.create_user(
            UserCreate(
                email="candy@example.com",
                full_name="Candy Hernández",
                language="es"
            )
        )
        print(f"Created user: {user.id}")
        ```
        """
        user = User(**user_data.model_dump())
        self.db.add(user)
        await self.db.flush()  # Get ID without committing
        await self.db.refresh(user)  # Load default values
        return user
    
    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User UUID
            
        Returns:
            User if found, None otherwise
            
        Example:
        ```python
        user = await service.get_user_by_id(user_id)
        if user:
            print(f"Found: {user.full_name}")
        ```
        """
        stmt = select(User).where(
            User.id == user_id,
            User.deleted_at.is_(None)  # Only active users
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            email: User email address
            
        Returns:
            User if found, None otherwise
            
        Example:
        ```python
        user = await service.get_user_by_email("candy@example.com")
        ```
        """
        stmt = select(User).where(
            User.email == email,
            User.deleted_at.is_(None)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all_users(self, include_deleted: bool = False) -> List[User]:
        """
        Get all users.
        
        Args:
            include_deleted: Include soft-deleted users
            
        Returns:
            List of users
            
        Example:
        ```python
        # Active users only
        users = await service.get_all_users()
        
        # Include deleted
        all_users = await service.get_all_users(include_deleted=True)
        ```
        """
        stmt = select(User)
        if not include_deleted:
            stmt = stmt.where(User.deleted_at.is_(None))
        
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> Optional[User]:
        """
        Update user.
        
        Args:
            user_id: User UUID
            user_data: Fields to update
            
        Returns:
            Updated user if found, None otherwise
            
        Example:
        ```python
        user = await service.update_user(
            user_id,
            UserUpdate(full_name="Candy Hernández-Ramirez")
        )
        ```
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        
        # Update only provided fields
        for field, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        
        await self.db.flush()
        await self.db.refresh(user)
        return user
    
    async def soft_delete_user(self, user_id: UUID) -> bool:
        """
        Soft delete a user.
        
        Args:
            user_id: User UUID
            
        Returns:
            True if deleted, False if not found
            
        Example:
        ```python
        success = await service.soft_delete_user(user_id)
        if success:
            print("User deleted")
        ```
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.soft_delete()
        await self.db.flush()
        return True
    
    async def restore_user(self, user_id: UUID) -> bool:
        """
        Restore a soft-deleted user.
        
        Args:
            user_id: User UUID
            
        Returns:
            True if restored, False if not found
        """
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user or not user.is_deleted:
            return False
        
        user.restore()
        await self.db.flush()
        return True


class FamilyService:
    """
    Service for family-related operations.
    
    Handles:
    - Creating families
    - Adding members
    - Removing members
    - Querying family data
    """
    
    def __init__(self, db: AsyncSession):
        """Initialize service with database session."""
        self.db = db
    
    async def create_family(self, family_data: FamilyCreate) -> Family:
        """
        Create a new family.
        
        Example:
        ```python
        family = await service.create_family(
            FamilyCreate(name="Family CH")
        )
        ```
        """
        family = Family(**family_data.model_dump())
        self.db.add(family)
        await self.db.flush()
        await self.db.refresh(family)
        return family
    
    async def add_member(
        self,
        family_id: UUID,
        user_id: UUID,
        role: str = "member"
    ) -> FamilyMembership:
        """
        Add a user to a family.
        
        Args:
            family_id: Family UUID
            user_id: User UUID
            role: User role (admin | member)
            
        Returns:
            FamilyMembership record
            
        Example:
        ```python
        membership = await service.add_member(
            family_id=family.id,
            user_id=user.id,
            role="admin"
        )
        ```
        """
        membership = FamilyMembership(
            family_id=family_id,
            user_id=user_id,
            role=role
        )
        self.db.add(membership)
        await self.db.flush()
        await self.db.refresh(membership)
        return membership
    
    async def get_family_members(self, family_id: UUID) -> List[FamilyMembership]:
        """
        Get all members of a family.
        
        Example:
        ```python
        members = await service.get_family_members(family_id)
        for member in members:
            print(f"{member.user.full_name} - {member.role}")
        ```
        """
        stmt = select(FamilyMembership).where(
            FamilyMembership.family_id == family_id
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def get_user_families(self, user_id: UUID) -> List[Family]:
        """
        Get all families a user belongs to.
        
        Example:
        ```python
        families = await service.get_user_families(user_id)
        for family in families:
            print(family.name)
        ```
        """
        stmt = (
            select(Family)
            .join(FamilyMembership)
            .where(FamilyMembership.user_id == user_id)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
