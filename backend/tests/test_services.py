"""
Service Layer Tests

Unit tests for service classes (UserService, RoutineService, HabitService).

These tests verify:
- CRUD operations work correctly
- Business logic is implemented correctly
- Error handling works
- Database transactions are handled properly

Target: 80% coverage for service layer
"""

import pytest
from uuid import UUID

from app.models import User
from app.services import UserService, RoutineService, HabitService
from app.schemas import UserCreate, UserUpdate, UserSignup


# =============================================================================
# UserService Tests
# =============================================================================

@pytest.mark.asyncio
async def test_create_user(db_session):
    """Test creating a user without password."""
    service = UserService(db_session)
    
    user_data = UserCreate(
        email="test@example.com",
        full_name="Test User",
        language="en"
    )
    
    user = await service.create_user(user_data)
    await db_session.commit()
    
    assert user is not None
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.hashed_password is None  # No password set


@pytest.mark.asyncio
async def test_create_user_with_password(db_session):
    """Test creating a user with password."""
    service = UserService(db_session)
    
    user_data = UserSignup(
        email="password@example.com",
        password="SecurePassword123!",
        full_name="Password User",
        language="en"
    )
    
    user = await service.create_user_with_password(user_data)
    await db_session.commit()
    
    assert user is not None
    assert user.email == "password@example.com"
    assert user.hashed_password is not None
    assert user.hashed_password.startswith("$2b$")  # bcrypt hash


@pytest.mark.asyncio
async def test_get_user_by_id(db_session, test_user):
    """Test getting user by ID."""
    service = UserService(db_session)
    
    user = await service.get_user_by_id(test_user.id)
    
    assert user is not None
    assert user.id == test_user.id
    assert user.email == test_user.email


@pytest.mark.asyncio
async def test_get_user_by_email(db_session, test_user):
    """Test getting user by email."""
    service = UserService(db_session)
    
    user = await service.get_user_by_email(test_user.email)
    
    assert user is not None
    assert user.email == test_user.email


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(db_session):
    """Test getting non-existent user by email."""
    service = UserService(db_session)
    
    user = await service.get_user_by_email("nonexistent@example.com")
    
    assert user is None


@pytest.mark.asyncio
async def test_authenticate_user_success(db_session, test_user):
    """Test successful user authentication."""
    service = UserService(db_session)
    
    user = await service.authenticate_user(
        test_user.email,
        "TestPassword123!"  # Password from test_user fixture
    )
    
    assert user is not None
    assert user.id == test_user.id


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(db_session, test_user):
    """Test authentication with wrong password."""
    service = UserService(db_session)
    
    user = await service.authenticate_user(
        test_user.email,
        "WrongPassword123!"
    )
    
    assert user is None


@pytest.mark.asyncio
async def test_authenticate_user_not_found(db_session):
    """Test authentication with non-existent user."""
    service = UserService(db_session)
    
    user = await service.authenticate_user(
        "nonexistent@example.com",
        "SomePassword123!"
    )
    
    assert user is None


@pytest.mark.asyncio
async def test_update_user(db_session, test_user):
    """Test updating a user."""
    service = UserService(db_session)
    
    update_data = UserUpdate(full_name="Updated Name")
    updated_user = await service.update_user(test_user.id, update_data)
    await db_session.commit()
    
    assert updated_user is not None
    assert updated_user.full_name == "Updated Name"
    assert updated_user.email == test_user.email  # Unchanged


@pytest.mark.asyncio
async def test_update_user_not_found(db_session):
    """Test updating non-existent user."""
    from uuid import uuid4
    
    service = UserService(db_session)
    
    update_data = UserUpdate(full_name="Updated Name")
    updated_user = await service.update_user(uuid4(), update_data)
    
    assert updated_user is None


@pytest.mark.asyncio
async def test_soft_delete_user(db_session, test_user):
    """Test soft deleting a user."""
    service = UserService(db_session)
    
    success = await service.soft_delete_user(test_user.id)
    await db_session.commit()
    
    assert success is True
    
    # User should still exist but be marked as deleted
    user = await service.get_user_by_id(test_user.id)
    assert user is None  # get_user_by_id excludes deleted users
    
    # But we can still find it if we include deleted
    from sqlalchemy import select
    stmt = select(User).where(User.id == test_user.id)
    result = await db_session.execute(stmt)
    deleted_user = result.scalar_one_or_none()
    assert deleted_user is not None
    assert deleted_user.is_deleted is True


@pytest.mark.asyncio
async def test_restore_user(db_session, test_user):
    """Test restoring a soft-deleted user."""
    service = UserService(db_session)
    
    # First delete
    await service.soft_delete_user(test_user.id)
    await db_session.commit()
    
    # Then restore
    success = await service.restore_user(test_user.id)
    await db_session.commit()
    
    assert success is True
    
    # User should be accessible again
    user = await service.get_user_by_id(test_user.id)
    assert user is not None
    assert user.is_deleted is False
