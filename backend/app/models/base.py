"""
Base Models and Mixins

This module provides base classes and mixins for SQLAlchemy models.
All models inherit common patterns for UUIDs, timestamps, and soft deletes.

Why Mixins?
- DRY (Don't Repeat Yourself): Common fields defined once
- Consistency: All models have same timestamp behavior
- Type safety: mypy knows about these fields
- Easy to extend: Add new mixins as needed

See: https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html
"""

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    
    This provides the foundation for all database tables.
    Uses SQLAlchemy 2.0 declarative style with type annotations.
    
    See: https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html
    """
    pass


class UUIDMixin:
    """
    Mixin for UUID primary key.
    
    All tables use UUID as primary key for:
    - Security: No sequential IDs exposed
    - Distributed systems: No ID collisions
    - Better for privacy
    
    Usage:
    ```python
    class User(Base, UUIDMixin):
        __tablename__ = "users"
        email: Mapped[str]
    ```
    
    This automatically adds:
    - id: UUID = Column(UUID, primary_key=True, default=uuid4)
    """
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )


class TimestampMixin:
    """
    Mixin for created_at and updated_at timestamps.
    
    Automatically tracks:
    - created_at: When record was created
    - updated_at: When record was last modified
    
    Both timestamps are:
    - In UTC (convert to user's timezone for display)
    - Managed by database (accurate even with multiple app servers)
    - Indexed for efficient queries
    
    Usage:
    ```python
    class User(Base, UUIDMixin, TimestampMixin):
        __tablename__ = "users"
        email: Mapped[str]
    ```
    
    This automatically adds:
    - created_at: datetime (set on insert)
    - updated_at: datetime (updated on every change)
    """
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # Database sets this
        nullable=False,
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),  # Database updates this automatically
        nullable=False,
    )


class SoftDeleteMixin:
    """
    Mixin for soft delete functionality.
    
    Soft delete = don't actually delete, just mark as deleted.
    
    Why soft delete?
    - Audit trail: Can see what was deleted and when
    - Recovery: Can restore accidentally deleted data
    - Referential integrity: Related records still link correctly
    - Analytics: Include/exclude deleted items in reports
    
    Usage:
    ```python
    class User(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
        __tablename__ = "users"
        email: Mapped[str]
    ```
    
    Querying:
    ```python
    # Active users only (default)
    active_users = select(User).where(User.deleted_at.is_(None))
    
    # Include deleted users
    all_users = select(User)
    
    # Soft delete a user
    user.deleted_at = datetime.utcnow()
    await session.commit()
    ```
    """
    
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )
    
    @property
    def is_deleted(self) -> bool:
        """Check if this record is soft-deleted."""
        return self.deleted_at is not None
    
    def soft_delete(self) -> None:
        """Mark this record as deleted."""
        self.deleted_at = datetime.utcnow()
    
    def restore(self) -> None:
        """Restore a soft-deleted record."""
        self.deleted_at = None


class BaseModel(Base, UUIDMixin, TimestampMixin):
    """
    Base model with UUID and timestamps.
    
    Most models should inherit from this.
    
    Usage:
    ```python
    class User(BaseModel):
        __tablename__ = "users"
        email: Mapped[str]
        full_name: Mapped[str]
    ```
    
    This gives you:
    - id: UUID primary key
    - created_at: timestamp
    - updated_at: timestamp
    """
    
    __abstract__ = True  # Don't create a table for this class
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<{self.__class__.__name__}(id={self.id})>"


class BaseModelWithSoftDelete(BaseModel, SoftDeleteMixin):
    """
    Base model with UUID, timestamps, and soft delete.
    
    Use this for models that need soft delete functionality.
    
    Usage:
    ```python
    class User(BaseModelWithSoftDelete):
        __tablename__ = "users"
        email: Mapped[str]
    ```
    
    This gives you:
    - id: UUID primary key
    - created_at: timestamp
    - updated_at: timestamp
    - deleted_at: timestamp (NULL = active)
    - is_deleted property
    - soft_delete() method
    - restore() method
    """
    
    __abstract__ = True  # Don't create a table for this class
