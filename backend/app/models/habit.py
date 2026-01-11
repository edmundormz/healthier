"""
Habit Models

These models represent the habit tracking system.

Database Tables:
- habits: Habit definitions
- habit_logs: Daily habit completions
- habit_streaks: Calculated streak data

Relationships:
- Habit → many habit_logs
- Habit → one habit_streak
"""

from datetime import date, datetime
from decimal import Decimal
from enum import Enum as PyEnum
from typing import List, Optional
from uuid import UUID

from sqlalchemy import (
    String, Text, Boolean, Date, DateTime, Numeric,
    ForeignKey, Enum as SAEnum, UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


# =============================================================================
# Enums
# =============================================================================

class HabitType(str, PyEnum):
    """
    Type of habit tracking.
    
    Values:
        boolean: Simple yes/no completion (e.g., "Took vitamins")
        numeric: Track a number (e.g., "10,000 steps", "8 glasses water")
    """
    boolean = "boolean"
    numeric = "numeric"


# =============================================================================
# Models
# =============================================================================

class Habit(BaseModel):
    """
    Habit model - Habit definitions.
    
    Represents a habit that users track daily.
    
    Attributes:
        user_id: Owner of this habit
        name: Habit name (e.g., "Walk 10k steps")
        type: boolean or numeric
        target_value: Target for numeric habits
        unit: Unit for numeric habits (e.g., "steps", "glasses")
        active: Whether this habit is currently being tracked
        
    Relationships:
        user: The user who owns this habit
        logs: List of habit logs
        streak: Current streak data
        
    Example:
    ```python
    # Boolean habit
    habit = Habit(
        user_id=user.id,
        name="Take vitamins",
        type=HabitType.boolean,
        active=True
    )
    
    # Numeric habit
    habit = Habit(
        user_id=user.id,
        name="Walk 10k steps",
        type=HabitType.numeric,
        target_value=10000,
        unit="steps",
        active=True
    )
    session.add(habit)
    await session.commit()
    ```
    """
    
    __tablename__ = "habits"
    
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    type: Mapped[HabitType] = mapped_column(
        SAEnum(HabitType, name="habit_type"),
        default=HabitType.boolean,
        nullable=False,
    )
    
    target_value: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )
    
    unit: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    
    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
    )
    
    # Relationships
    logs: Mapped[List["HabitLog"]] = relationship(
        "HabitLog",
        back_populates="habit",
        cascade="all, delete-orphan",
        order_by="HabitLog.log_date.desc()",
    )
    
    streak: Mapped[Optional["HabitStreak"]] = relationship(
        "HabitStreak",
        back_populates="habit",
        uselist=False,  # One-to-one relationship
        cascade="all, delete-orphan",
    )
    
    def __repr__(self) -> str:
        return f"<Habit(id={self.id}, name='{self.name}', type={self.type.value})>"


class HabitLog(BaseModel):
    """
    HabitLog model - Daily habit completion.
    
    Records whether a habit was completed on a specific day.
    
    Attributes:
        habit_id: The habit being logged
        user_id: User who logged this
        log_date: Date of the log
        completed: Whether habit was completed (for boolean habits)
        value: Value logged (for numeric habits)
        logged_at: Timestamp when logged
        notes: Optional notes
        
    Relationships:
        habit: The habit
        user: The user
        
    Constraints:
        - Unique (habit_id, log_date)
        - One log per habit per day
        
    Example:
    ```python
    # Boolean habit log
    log = HabitLog(
        habit_id=habit.id,
        user_id=user.id,
        log_date=date.today(),
        completed=True
    )
    
    # Numeric habit log
    log = HabitLog(
        habit_id=habit.id,
        user_id=user.id,
        log_date=date.today(),
        value=12500,  # steps
        completed=True,
        notes="Walked to the park"
    )
    session.add(log)
    await session.commit()
    ```
    """
    
    __tablename__ = "habit_logs"
    __table_args__ = (
        UniqueConstraint("habit_id", "log_date", name="uq_habit_log"),
    )
    
    habit_id: Mapped[UUID] = mapped_column(
        ForeignKey("habits.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    
    log_date: Mapped[date] = mapped_column(
        Date,
        default=date.today,
        nullable=False,
        index=True,
    )
    
    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    
    value: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )
    
    logged_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Relationships
    habit: Mapped["Habit"] = relationship(
        "Habit",
        back_populates="logs",
    )
    
    def __repr__(self) -> str:
        status = "✓" if self.completed else "✗"
        return f"<HabitLog(id={self.id}, date={self.log_date}, completed={status})>"


class HabitStreak(BaseModel):
    """
    HabitStreak model - Calculated streak data.
    
    Tracks current and longest streaks for a habit.
    This is a computed/cached table that gets updated when habits are logged.
    
    Attributes:
        habit_id: The habit
        user_id: The user
        current_streak: Current consecutive days
        longest_streak: Best streak ever achieved
        last_completed_date: Last date habit was completed
        
    Relationships:
        habit: The habit
        user: The user
        
    Constraints:
        - Unique (habit_id, user_id)
        
    Example:
    ```python
    # Query streak
    stmt = select(HabitStreak).where(
        HabitStreak.habit_id == habit.id,
        HabitStreak.user_id == user.id
    )
    streak = (await session.execute(stmt)).scalar_one()
    
    print(f"Current: {streak.current_streak} days")
    print(f"Best: {streak.longest_streak} days")
    
    # Update streak (typically done via service layer)
    streak.current_streak += 1
    if streak.current_streak > streak.longest_streak:
        streak.longest_streak = streak.current_streak
    streak.last_completed_date = date.today()
    await session.commit()
    ```
    """
    
    __tablename__ = "habit_streaks"
    __table_args__ = (
        UniqueConstraint("habit_id", "user_id", name="uq_habit_streak"),
    )
    
    habit_id: Mapped[UUID] = mapped_column(
        ForeignKey("habits.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    
    current_streak: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )
    
    longest_streak: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )
    
    last_completed_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )
    
    # Relationships
    habit: Mapped["Habit"] = relationship(
        "Habit",
        back_populates="streak",
    )
    
    def __repr__(self) -> str:
        return f"<HabitStreak(habit_id={self.habit_id}, current={self.current_streak}, best={self.longest_streak})>"
