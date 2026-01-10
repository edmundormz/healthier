"""
Database Connection and Session Management

This module sets up SQLAlchemy for async database operations with Supabase Postgres.

Why async?
- Non-blocking database operations
- Better performance under load
- Allows FastAPI to handle multiple requests concurrently

See: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base
import structlog

from app.core.config import settings

logger = structlog.get_logger()

# Create the async engine
# This manages the connection pool to the database
# Connection pool = reusable database connections (faster than creating new ones each time)
# See: https://docs.sqlalchemy.org/en/20/core/engines.html
engine = create_async_engine(
    # Convert Supabase URL to async format
    # postgresql:// -> postgresql+asyncpg://
    settings.SUPABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.DEBUG,  # Log all SQL queries in debug mode
    pool_size=5,  # Number of connections to keep in pool
    max_overflow=10,  # Allow 10 extra connections if needed
    pool_pre_ping=True,  # Verify connections before using them
)

# Create session factory
# This is used to create database sessions (transactions)
# expire_on_commit=False means objects are still usable after commit
# See: https://docs.sqlalchemy.org/en/20/orm/session_api.html
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for all SQLAlchemy models
# All database models will inherit from this
# This provides common functionality like __repr__, __tablename__, etc.
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function that provides a database session.
    
    This is used as a FastAPI dependency:
    ```python
    @app.get("/users")
    async def get_users(db: AsyncSession = Depends(get_db)):
        # db is automatically provided and cleaned up
        pass
    ```
    
    Why use this pattern?
    - Automatically opens and closes database connections
    - Ensures transactions are committed or rolled back
    - Prevents connection leaks
    - Makes testing easier (can mock the database)
    
    Yields:
        AsyncSession: Database session
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


async def init_db():
    """
    Initialize database tables.
    
    In production, we use migrations (Alembic) instead of this.
    This is useful for:
    - Local development
    - Testing
    - Initial setup
    
    Note: This creates tables based on SQLAlchemy models.
    It does NOT create indexes, constraints, or RLS policies.
    Those are handled by SQL migrations.
    """
    async with engine.begin() as conn:
        # Create all tables defined in models
        # This only creates tables that don't exist yet
        await conn.run_sync(Base.metadata.create_all)
        
    logger.info("database_initialized")


async def close_db():
    """
    Close all database connections.
    
    Call this on application shutdown to cleanly close connections.
    This prevents "too many connections" errors.
    """
    await engine.dispose()
    logger.info("database_connections_closed")
