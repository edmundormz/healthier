"""
Routine Models

These models represent the routine system with version control and expiration.

Database Tables:
- routines: Container for routine versions
- routine_versions: Time-bound routine definitions
- routine_cards: Groups items by moment of day
- routine_items: Individual tasks (meds, supplements, habits)
- routine_completions: Daily check-ins

Relationships:
- Routine → many routine_versions
- RoutineVersion → many routine_cards
- RoutineCard → many routine_items
- RoutineItem → many routine_completions
"""

from datetime import date, datetime
from enum import Enum as PyEnum
from typing import List, Optional
from uuid import UUID

from sqlalchemy import (
    String, Text, Integer, Date, ForeignKey, Boolean,
    DateTime, Enum as SAEnum, UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


# =============================================================================
# Enums
# =============================================================================

class MomentOfDay(str, PyEnum):
    """
    Moment of day for routine cards.
    
    Values:
        MORNING: Morning routine (wake up, breakfast)
        MIDDAY: Midday routine (lunch, afternoon)
        EVENING: Evening routine (dinner, wind down)
        NIGHT: Night routine (bedtime)
    """
    MORNING = "MORNING"
    MIDDAY = "MIDDAY"
    EVENING = "EVENING"
    NIGHT = "NIGHT"


class RoutineItemType(str, PyEnum):
    """
    Type of routine item.
    
    Values:
        medication: Prescription medications
        supplement: Vitamins, supplements
        skincare: Skincare products
        hair_care: Hair care products
        habit: Habit tracking
    """
    medication = "medication"
    supplement = "supplement"
    skincare = "skincare"
    hair_care = "hair_care"
    habit = "habit"


# =============================================================================
# Models
# =============================================================================

class Routine(BaseModel):
    """
    Routine model - Container for routine versions.
    
    A routine has multiple versions over time as protocols change.
    
    Attributes:
        user_id: Owner of this routine
        name: Routine name (e.g., "Morning Routine")
        description: Optional description
        active_version_id: Current active version (nullable)
        
    Relationships:
        user: The user who owns this routine
        versions: List of routine versions
        active_version: The current active version
        
    Example:
    ```python
    # Create routine
    routine = Routine(
        user_id=user.id,
        name="Morning Routine",
        description="Daily morning protocol"
    )
    session.add(routine)
    await session.commit()
    ```
    """
    
    __tablename__ = "routines"
    
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    active_version_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("routine_versions.id"),
        nullable=True,
    )
    
    # Relationships
    versions: Mapped[List["RoutineVersion"]] = relationship(
        "RoutineVersion",
        back_populates="routine",
        cascade="all, delete-orphan",
        foreign_keys="RoutineVersion.routine_id",
    )
    
    def __repr__(self) -> str:
        return f"<Routine(id={self.id}, name='{self.name}')>"


class RoutineVersion(BaseModel):
    """
    RoutineVersion model - Time-bound routine definition.
    
    Each version is active for a date range. This allows tracking
    protocol changes over time (e.g., new medication, dosage change).
    
    Attributes:
        routine_id: Parent routine
        version_number: Sequential version number
        start_date: When this version becomes active
        end_date: When this version ends (NULL = ongoing)
        created_by: User who created this version
        notes: Reason for version change
        
    Relationships:
        routine: Parent routine
        cards: Routine cards for this version
        
    Constraints:
        - Unique (routine_id, version_number)
        
    Example:
    ```python
    # Create new version
    version = RoutineVersion(
        routine_id=routine.id,
        version_number=2,
        start_date=date.today(),
        notes="New protocol from Dr. Smith"
    )
    session.add(version)
    await session.commit()
    ```
    """
    
    __tablename__ = "routine_versions"
    __table_args__ = (
        UniqueConstraint("routine_id", "version_number", name="uq_routine_version"),
    )
    
    routine_id: Mapped[UUID] = mapped_column(
        ForeignKey("routines.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    version_number: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )
    
    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )
    
    end_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        index=True,
    )
    
    created_by: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )
    
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Relationships
    routine: Mapped["Routine"] = relationship(
        "Routine",
        back_populates="versions",
        foreign_keys=[routine_id],
    )
    
    cards: Mapped[List["RoutineCard"]] = relationship(
        "RoutineCard",
        back_populates="version",
        cascade="all, delete-orphan",
    )
    
    def __repr__(self) -> str:
        return f"<RoutineVersion(id={self.id}, routine_id={self.routine_id}, v{self.version_number})>"


class RoutineCard(BaseModel):
    """
    RoutineCard model - Groups items by moment of day.
    
    Each card represents a time of day (morning, midday, evening, night)
    and contains multiple routine items.
    
    Attributes:
        routine_version_id: Parent routine version
        moment: Time of day (MORNING | MIDDAY | EVENING | NIGHT)
        sort_order: Display order
        
    Relationships:
        version: Parent routine version
        items: Routine items in this card
        
    Example:
    ```python
    # Create morning card
    card = RoutineCard(
        routine_version_id=version.id,
        moment=MomentOfDay.MORNING,
        sort_order=0
    )
    session.add(card)
    await session.commit()
    ```
    """
    
    __tablename__ = "routine_cards"
    
    routine_version_id: Mapped[UUID] = mapped_column(
        ForeignKey("routine_versions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    moment: Mapped[MomentOfDay] = mapped_column(
        SAEnum(MomentOfDay, name="moment_of_day"),
        nullable=False,
    )
    
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    # Relationships
    version: Mapped["RoutineVersion"] = relationship(
        "RoutineVersion",
        back_populates="cards",
    )
    
    items: Mapped[List["RoutineItem"]] = relationship(
        "RoutineItem",
        back_populates="card",
        cascade="all, delete-orphan",
    )
    
    def __repr__(self) -> str:
        return f"<RoutineCard(id={self.id}, moment={self.moment.value})>"


class RoutineItem(BaseModel):
    """
    RoutineItem model - Individual task in a routine.
    
    Represents medications, supplements, skincare, or habits.
    Items can expire or transition to other items.
    
    Attributes:
        routine_card_id: Parent routine card
        type: Type of item (medication | supplement | etc.)
        name: Item name (e.g., "Metformin")
        dosage: Dosage info (e.g., "500mg")
        instructions: How to take (e.g., "With breakfast")
        frequency: How often (daily | weekdays | custom)
        expires_at: When this item expires (NULL = never)
        duration_days: Alternative to expires_at
        next_item_id: Item to transition to after expiration
        sort_order: Display order
        
    Relationships:
        card: Parent routine card
        completions: Completion records
        next_item: Next item in transition chain
        
    Example:
    ```python
    # Create medication item
    item = RoutineItem(
        routine_card_id=card.id,
        type=RoutineItemType.medication,
        name="Metformin",
        dosage="500mg",
        instructions="Take with breakfast",
        frequency="daily"
    )
    session.add(item)
    await session.commit()
    ```
    """
    
    __tablename__ = "routine_items"
    
    routine_card_id: Mapped[UUID] = mapped_column(
        ForeignKey("routine_cards.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    type: Mapped[RoutineItemType] = mapped_column(
        SAEnum(RoutineItemType, name="routine_item_type"),
        nullable=False,
    )
    
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    dosage: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    
    instructions: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    frequency: Mapped[str] = mapped_column(
        String(50),
        default="daily",
        nullable=False,
    )
    
    expires_at: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        index=True,
    )
    
    duration_days: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    
    next_item_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("routine_items.id"),
        nullable=True,
    )
    
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    # Relationships
    card: Mapped["RoutineCard"] = relationship(
        "RoutineCard",
        back_populates="items",
    )
    
    completions: Mapped[List["RoutineCompletion"]] = relationship(
        "RoutineCompletion",
        back_populates="item",
        cascade="all, delete-orphan",
    )
    
    next_item: Mapped[Optional["RoutineItem"]] = relationship(
        "RoutineItem",
        remote_side="RoutineItem.id",
        foreign_keys=[next_item_id],
    )
    
    def __repr__(self) -> str:
        return f"<RoutineItem(id={self.id}, name='{self.name}', type={self.type.value})>"


class RoutineCompletion(BaseModel):
    """
    RoutineCompletion model - Daily check-in for routine items.
    
    Tracks whether a user completed a routine item on a specific day.
    
    Attributes:
        user_id: User who completed (or skipped) the item
        routine_item_id: The routine item
        completed_at: Timestamp of completion
        completion_date: Date of completion (for queries)
        notes: Optional notes
        skipped: Whether item was skipped
        skip_reason: Why item was skipped
        
    Relationships:
        user: The user
        item: The routine item
        
    Constraints:
        - Unique (user_id, routine_item_id, completion_date)
        - One completion per item per day
        
    Example:
    ```python
    # Complete item
    completion = RoutineCompletion(
        user_id=user.id,
        routine_item_id=item.id,
        completion_date=date.today(),
        skipped=False
    )
    session.add(completion)
    await session.commit()
    
    # Skip item
    completion = RoutineCompletion(
        user_id=user.id,
        routine_item_id=item.id,
        completion_date=date.today(),
        skipped=True,
        skip_reason="Felt nauseous"
    )
    session.add(completion)
    await session.commit()
    ```
    """
    
    __tablename__ = "routine_completions"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "routine_item_id", "completion_date",
            name="uq_routine_completion"
        ),
    )
    
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    
    routine_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("routine_items.id"),
        nullable=False,
        index=True,
    )
    
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    
    completion_date: Mapped[date] = mapped_column(
        Date,
        default=date.today,
        nullable=False,
        index=True,
    )
    
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    skipped: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    
    skip_reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Relationships
    item: Mapped["RoutineItem"] = relationship(
        "RoutineItem",
        back_populates="completions",
    )
    
    def __repr__(self) -> str:
        status = "skipped" if self.skipped else "completed"
        return f"<RoutineCompletion(id={self.id}, date={self.completion_date}, status={status})>"
