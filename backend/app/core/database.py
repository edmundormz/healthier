"""
Database Connection and Session Management

This module sets up SQLAlchemy async engine and session management for Supabase Postgres.

Why SQLAlchemy ORM?
- Type safety with Python models that map to database tables
- IDE autocomplete and refactoring support
- Prevents SQL injection (uses parameterized queries)
- Relationship management (user.families, routine.items, etc.)
- Transaction support for data integrity
- Migration tracking with Alembic

Architecture:
    FastAPI → SQLAlchemy ORM → asyncpg driver → Supabase Postgres

See: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase
import structlog

from app.core.config import settings

logger = structlog.get_logger()


# =============================================================================
# SQLAlchemy Base Model
# =============================================================================

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    
    All your models will inherit from this class:
    
    ```python
    class User(Base):
        __tablename__ = "users"
        id = Column(UUID, primary_key=True)
        email = Column(String, unique=True)
    ```
    
    This base class provides:
    - Table metadata tracking
    - Relationship configuration
    - Migration support
    """
    pass


# =============================================================================
# Database Engine Configuration
# =============================================================================

# Create async engine
# This manages the connection pool to the database
# See: https://docs.sqlalchemy.org/en/20/core/engines.html
#
# IMPORTANT: For async operations, use DIRECT_URL instead of pooled DATABASE_URL
# asyncpg doesn't work with Supabase's connection pooler (pgbouncer parameter)
# DIRECT_URL connects directly to Postgres without pooling
# The SQLAlchemy engine provides its own connection pooling
engine = create_async_engine(
    settings.DIRECT_URL,
    echo=settings.DEBUG,  # Log SQL queries in development
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=5,  # Number of connections to maintain
    max_overflow=10,  # Additional connections if pool is full
    pool_recycle=3600,  # Recycle connections after 1 hour (prevents stale connections)
    connect_args={
        "statement_cache_size": 0,  # Disable prepared statements for compatibility
    },
)

# Create session factory
# Sessions are used to interact with the database
# Each request gets its own session
# See: https://docs.sqlalchemy.org/en/20/orm/session_api.html
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit (better for async)
    autocommit=False,  # Explicit commits required (safer)
    autoflush=False,  # Explicit flushes required (more control)
)


# =============================================================================
# Dependency Injection
# =============================================================================

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides a database session.
    
    This is used in your API endpoints:
    
    ```python
    @app.get("/users")
    async def get_users(db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(User))
        users = result.scalars().all()
        return users
    ```
    
    The session is automatically:
    - Created before the request
    - Committed if successful
    - Rolled back on error
    - Closed after the request
    
    Yields:
        AsyncSession: Database session for this request
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# =============================================================================
# Database Utilities
# =============================================================================

async def init_db() -> None:
    """
    Initialize database tables.
    
    Note: In production, we use Alembic migrations instead.
    This function is useful for testing or initial setup.
    
    In development:
    - Tables already exist in Supabase (created via migrations)
    - This function verifies the connection works
    
    Usage:
    ```python
    await init_db()  # Verifies tables exist
    ```
    """
    async with engine.begin() as conn:
        # Verify connection works
        # In production, use Alembic migrations to create/update tables
        # await conn.run_sync(Base.metadata.create_all)
        logger.info("database_initialized", note="Using existing Supabase schema")


async def test_connection() -> bool:
    """
    Test database connection.
    
    This performs a simple query to verify:
    - Database is accessible
    - Credentials are correct
    - Network connection works
    
    Returns:
        bool: True if connection successful, False otherwise
        
    Example:
    ```python
    if await test_connection():
        print("✅ Database connected")
    else:
        print("❌ Database connection failed")
    ```
    """
    try:
        async with AsyncSessionLocal() as session:
            # Simple query to test connection
            result = await session.execute(text("SELECT 1"))
            result.scalar()
            logger.info("database_connection_test_successful")
            return True
    except Exception as e:
        logger.error("database_connection_test_failed", error=str(e))
        return False


async def close_db() -> None:
    """
    Close database connections.
    
    This is called during application shutdown to:
    - Close all active connections
    - Release connection pool resources
    - Cleanup async tasks
    
    FastAPI calls this automatically via lifespan handler.
    """
    await engine.dispose()
    logger.info("database_connections_closed")


# =============================================================================
# Import fix for test_connection
# =============================================================================

from sqlalchemy import text  # noqa: E402
