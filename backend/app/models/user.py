"""
User and Family Models

These models represent users, families, and their relationships.

Database Tables:
- users: Individual users (Candy, Héctor)
- families: Family groups (Family CH)
- family_memberships: Links users to families (many-to-many)

Relationships:
- User has many family_memberships
- Family has many family_memberships
- User → family_memberships → Family (many-to-many through membership)
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModelWithSoftDelete, BaseModel


class User(BaseModelWithSoftDelete):
    """
    User model - Individual users in the system.
    
    Attributes:
        email: Unique email address (login identifier)
        full_name: User's full name (e.g., "Candy Hernández")
        timezone: User's timezone (default: America/Chicago)
        language: Preferred language (es | en)
        notification_enabled: Whether to send notifications
        last_active_at: Last time user was active
        
    Relationships:
        families: List of families this user belongs to
        family_memberships: List of FamilyMembership objects
        routines: User's routines
        habits: User's habits
        
    Soft Delete:
        - Uses deleted_at timestamp
        - Deleted users can be restored
        - Related data is preserved
    
    Example:
    ```python
    # Create user
    user = User(
        email="candy@example.com",
        full_name="Candy Hernández",
        language="es"
    )
    session.add(user)
    await session.commit()
    
    # Query user
    stmt = select(User).where(User.email == "candy@example.com")
    user = (await session.execute(stmt)).scalar_one()
    
    # Access families
    for family in user.families:
        print(family.name)
    ```
    """
    
    __tablename__ = "users"
    
    # Core fields
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    
    # Password (hashed, never store plain text!)
    # This field is nullable to support existing users and optional auth methods
    hashed_password: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    timezone: Mapped[str] = mapped_column(
        String(50),
        default="America/Chicago",
        nullable=False,
    )
    
    # Preferences
    language: Mapped[str] = mapped_column(
        String(5),
        default="es",  # es | en
        nullable=False,
    )
    
    notification_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    
    # Activity tracking
    last_active_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Relationships
    # Note: These are defined as strings to avoid circular imports
    # SQLAlchemy resolves them at runtime
    family_memberships: Mapped[List["FamilyMembership"]] = relationship(
        "FamilyMembership",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<User(id={self.id}, email='{self.email}', name='{self.full_name}')>"


class Family(BaseModel):
    """
    Family model - Family groups.
    
    Attributes:
        name: Family name (e.g., "Family CH")
        
    Relationships:
        members: List of users in this family
        family_memberships: List of FamilyMembership objects
        
    Example:
    ```python
    # Create family
    family = Family(name="Family CH")
    session.add(family)
    await session.commit()
    
    # Add member
    membership = FamilyMembership(
        family_id=family.id,
        user_id=user.id,
        role="admin"
    )
    session.add(membership)
    await session.commit()
    ```
    """
    
    __tablename__ = "families"
    
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    # Relationships
    family_memberships: Mapped[List["FamilyMembership"]] = relationship(
        "FamilyMembership",
        back_populates="family",
        cascade="all, delete-orphan",
    )
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<Family(id={self.id}, name='{self.name}')>"


class FamilyMembership(BaseModel):
    """
    FamilyMembership model - Links users to families.
    
    This is a junction table for the many-to-many relationship
    between users and families.
    
    Attributes:
        family_id: Foreign key to families
        user_id: Foreign key to users
        role: User's role in family (admin | member)
        joined_at: When user joined the family
        
    Relationships:
        family: The family
        user: The user
        
    Constraints:
        - Unique constraint on (family_id, user_id)
        - User can only be in a family once
        
    Example:
    ```python
    # Create membership
    membership = FamilyMembership(
        family_id=family.id,
        user_id=user.id,
        role="admin"
    )
    session.add(membership)
    await session.commit()
    
    # Query family members
    stmt = select(FamilyMembership).where(
        FamilyMembership.family_id == family_id
    )
    memberships = (await session.execute(stmt)).scalars().all()
    
    for membership in memberships:
        print(f"{membership.user.full_name} - {membership.role}")
    ```
    """
    
    __tablename__ = "family_memberships"
    
    family_id: Mapped[UUID] = mapped_column(
        ForeignKey("families.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    role: Mapped[str] = mapped_column(
        String(20),
        default="member",  # admin | member
        nullable=False,
    )
    
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    
    # Relationships
    family: Mapped["Family"] = relationship(
        "Family",
        back_populates="family_memberships",
    )
    
    user: Mapped["User"] = relationship(
        "User",
        back_populates="family_memberships",
    )
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<FamilyMembership(user_id={self.user_id}, family_id={self.family_id}, role='{self.role}')>"
