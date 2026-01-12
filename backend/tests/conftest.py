"""
Pytest Configuration and Fixtures

This file contains shared fixtures for all tests.
Fixtures defined here are automatically available to all test files.

Why fixtures?
- Reusable test data and setup
- Clean test code (no duplication)
- Easy to maintain (change once, affects all tests)
- Automatic cleanup (teardown handled automatically)

See: https://docs.pytest.org/en/stable/fixture.html
"""

import pytest
from typing import AsyncGenerator
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.database import get_db, Base
from app.main import app
from app.models import User
from app.services import UserService
from app.core.security import hash_password


# =============================================================================
# Database Fixtures
# =============================================================================

@pytest.fixture(scope="session")
def test_database_url() -> str:
    """
    Get test database URL.
    
    In tests, we can use a separate test database or the same database
    with a test schema. For now, we'll use the same database but with
    careful cleanup.
    
    TODO: Set up a separate test database for CI/CD
    """
    # Use same database for now (we'll clean up after tests)
    # In production, use a separate test database
    return settings.DATABASE_URL


@pytest.fixture(scope="session")
async def test_engine():
    """
    Create test database engine.
    
    This engine is created once per test session and reused.
    """
    engine = create_async_engine(
        settings.DATABASE_URL,
        connect_args={"statement_cache_size": 0},  # pgbouncer compatibility
        echo=False,  # Set to True to see SQL queries in tests
    )
    
    yield engine
    
    # Cleanup: close engine after all tests
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Create a database session for each test.
    
    This fixture:
    1. Creates a new session for each test
    2. Starts a transaction
    3. Yields the session
    4. Rolls back the transaction (cleanup)
    
    This ensures tests don't affect each other.
    
    Usage:
    ```python
    async def test_something(db_session):
        # Use db_session here
        user = User(email="test@example.com", full_name="Test User")
        db_session.add(user)
        await db_session.commit()
    ```
    """
    # Create session factory
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        # Start a transaction
        async with session.begin():
            yield session
            # Rollback after test (cleanup)
            await session.rollback()


# =============================================================================
# Test Client Fixture
# =============================================================================

@pytest.fixture
def client(db_session: AsyncSession) -> TestClient:
    """
    Create a test client for FastAPI.
    
    This fixture:
    1. Overrides the database dependency
    2. Creates a test client
    3. Returns client for making HTTP requests
    
    Note: TestClient is synchronous, but we use async database sessions.
    FastAPI handles the async/sync bridge automatically.
    
    Usage:
    ```python
    def test_endpoint(client):
        response = client.get("/api/users/")
        assert response.status_code == 200
    ```
    """
    # Override database dependency to use test session
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client
    test_client = TestClient(app)
    
    yield test_client
    
    # Cleanup: remove dependency override
    app.dependency_overrides.clear()


# =============================================================================
# User Fixtures
# =============================================================================

@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """
    Create a test user.
    
    This fixture creates a user that can be used in tests.
    The user is automatically cleaned up after the test.
    
    Usage:
    ```python
    async def test_something(test_user):
        assert test_user.email == "test@example.com"
    ```
    """
    service = UserService(db_session)
    
    # Create user with password
    from app.schemas import UserSignup
    
    user_data = UserSignup(
        email="test@example.com",
        password="TestPassword123!",
        full_name="Test User",
        language="en"
    )
    
    user = await service.create_user_with_password(user_data)
    await db_session.commit()
    
    return user


@pytest.fixture
async def test_user_without_password(db_session: AsyncSession) -> User:
    """
    Create a test user without password.
    
    Useful for testing legacy users or optional auth methods.
    """
    service = UserService(db_session)
    
    from app.schemas import UserCreate
    
    user_data = UserCreate(
        email="nopassword@example.com",
        full_name="No Password User",
        language="en"
    )
    
    user = await service.create_user(user_data)
    await db_session.commit()
    
    return user


@pytest.fixture
def mock_supabase_client(monkeypatch, test_user):
    """
    Mock Supabase client for testing.
    
    This fixture mocks the Supabase client to avoid making real API calls
    during tests. It simulates Supabase Auth token validation.
    
    Usage:
    ```python
    def test_protected_endpoint(client, mock_supabase_client, test_user):
        # Test will use mocked Supabase client
        response = client.get("/api/routines/", headers=auth_headers)
    ```
    """
    from unittest.mock import Mock
    from app.core import supabase_auth
    
    # Mock verify_supabase_jwt to return test payload
    def mock_verify_jwt(token: str):
        """Mock JWT verification - returns payload for valid tokens."""
        if token.startswith("valid_"):
            # Extract user_id from token (format: "valid_{user_id}")
            user_id_str = token.replace("valid_", "")
            return {
                "sub": user_id_str,
                "email": test_user.email if hasattr(test_user, 'email') else "test@example.com",
                "role": "authenticated",
                "aud": "authenticated",
                "iss": "https://test.supabase.co/auth/v1"
            }
        return None
    
    monkeypatch.setattr(supabase_auth, "verify_supabase_jwt", mock_verify_jwt)
    
    return Mock()  # Return mock client object


@pytest.fixture
def auth_headers(test_user: User, mock_supabase_client) -> dict:
    """
    Create authentication headers for a test user with Supabase token.
    
    This fixture:
    1. Creates a mock Supabase JWT token for the test user
    2. Returns headers ready to use in requests
    
    Note: Uses mocked Supabase client, so no real API calls are made.
    
    Usage:
    ```python
    def test_protected_endpoint(client, auth_headers):
        response = client.get(
            "/api/routines/",
            headers=auth_headers
        )
        assert response.status_code == 200
    ```
    """
    # Create a mock Supabase token (starts with "valid_" to pass mock validation)
    # In real usage, this would be a Supabase JWT token
    token = f"valid_{test_user.id}"
    
    return {"Authorization": f"Bearer {token}"}
