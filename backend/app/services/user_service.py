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

from app.core.security import hash_password, verify_password
from app.models import User, Family, FamilyMembership
from app.schemas import (
    UserCreate,
    UserUpdate,
    FamilyCreate,
    FamilyMembershipCreate,
    UserSignup,
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
        Create a new user (without password).
        
        For user registration with password, use create_user_with_password().
        
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
    
    async def create_user_with_password(self, user_data: UserSignup) -> User:
        """
        Create a new user with password (for registration).
        
        This method:
        1. Hashes the password before storing
        2. Creates the user in database
        3. Never stores plain text password
        
        Args:
            user_data: User signup data (includes password)
            
        Returns:
            Created user (password is hashed)
            
        Example:
        ```python
        user = await service.create_user_with_password(
            UserSignup(
                email="candy@example.com",
                password="SecurePassword123!",
                full_name="Candy Hernández"
            )
        )
        ```
        """
        # Extract password and hash it
        password = user_data.password
        hashed = hash_password(password)
        
        # Create user data without password
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict["hashed_password"] = hashed
        
        # Create user
        user = User(**user_dict)
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password.
        
        This method:
        1. Finds user by email
        2. Verifies password against stored hash
        3. Returns user if authentication succeeds
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            User if authentication succeeds, None otherwise
            
        Example:
        ```python
        user = await service.authenticate_user(
            "candy@example.com",
            "SecurePassword123!"
        )
        if user:
            print("Login successful!")
        ```
        """
        user = await self.get_user_by_email(email)
        if not user:
            return None
        
        # Check if user has password set
        if not user.hashed_password:
            return None
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            return None
        
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
    
    async def sync_user_from_supabase(
        self,
        user_id: UUID,
        jwt_payload: dict
    ) -> Optional[User]:
        """
        Sync user from Supabase auth.users to public.users.
        
        When a user signs up via Supabase Auth, they exist in auth.users
        but not in public.users. This method creates/updates the user
        in public.users based on Supabase Auth data.
        
        Args:
            user_id: User UUID from Supabase Auth (from JWT 'sub' claim)
            jwt_payload: Decoded JWT payload from Supabase
            
        Returns:
            Synced User object, None if sync failed
            
        Example:
        ```python
        # User signs up via Supabase Auth
        # First API call with their token triggers sync
        user = await service.sync_user_from_supabase(user_id, jwt_payload)
        ```
        """
        # Extract user info from JWT payload
        email = jwt_payload.get("email", "")
        user_metadata = jwt_payload.get("user_metadata", {})
        full_name = user_metadata.get("full_name", email.split("@")[0] if email else "User")
        
        # Check if user already exists
        existing_user = await self.get_user_by_id(user_id)
        
        if existing_user:
            # Update existing user with latest info from Supabase
            existing_user.email = email
            existing_user.full_name = full_name
            # Update other fields from metadata if needed
            if "language" in user_metadata:
                existing_user.language = user_metadata["language"]
            if "timezone" in user_metadata:
                existing_user.timezone = user_metadata["timezone"]
            
            await self.db.flush()
            await self.db.refresh(existing_user)
            return existing_user
        
        # Create new user from Supabase Auth data
        from app.schemas import UserCreate
        
        user_data = UserCreate(
            email=email,
            full_name=full_name,
            language=user_metadata.get("language", "es"),
            timezone=user_metadata.get("timezone", "America/Chicago"),
        )
        
        # Create user with the same ID as Supabase Auth user
        user = User(
            id=user_id,  # Use same ID as auth.users
            **user_data.model_dump()
        )
        
        self.db.add(user)
        
        try:
            await self.db.flush()
            await self.db.refresh(user)
            return user
        except Exception as e:
            # Handle race condition: another parallel request may have created the user
            # Roll back and try to fetch the user again
            await self.db.rollback()
            
            # Try to fetch the user that was just created by the parallel request
            existing_user = await self.get_user_by_id(user_id)
            if existing_user:
                return existing_user
            
            # If still not found, re-raise the original error
            raise e


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
