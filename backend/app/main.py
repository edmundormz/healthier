"""
CH Health OS - Main FastAPI Application

This is the entry point for the CH Health OS API.
It sets up the FastAPI app, middleware, and routes.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from app.core.config import settings
from app.core.database import test_connection, close_db, init_db

# Initialize structured logging
# This provides JSON-formatted logs that are easier to parse and analyze
# See: https://www.structlog.org/
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI application.
    
    This replaces the deprecated @app.on_event() decorators.
    Code before 'yield' runs on startup, code after runs on shutdown.
    
    See: https://fastapi.tiangolo.com/advanced/events/#lifespan-events
    """
    # Startup code (runs when app starts)
    # Good place to:
    # - Initialize database connections
    # - Set up connection pools
    # - Load ML models
    # - Verify environment variables
    logger.info(
        "application_startup",
        environment=settings.ENVIRONMENT,
        debug=settings.DEBUG,
        database="SQLAlchemy + asyncpg + Supabase Postgres"
    )
    
    # Initialize database
    await init_db()
    
    # Test database connection
    db_connected = await test_connection()
    if db_connected:
        logger.info("database_connected", status="success", orm="SQLAlchemy 2.0")
    else:
        logger.warning("database_connection_failed", status="warning")
    
    yield  # Application runs here
    
    # Shutdown code (runs when app stops)
    # Good place to:
    # - Close database connections
    # - Cleanup resources
    # - Save state if needed
    await close_db()
    logger.info("application_shutdown")


# Create FastAPI application with lifespan handler
# OpenAPI docs will be available at /docs (Swagger UI) and /redoc (ReDoc)
app = FastAPI(
    title=settings.API_TITLE,
    description="Private, family-centered health operating system",
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,  # Use new lifespan handler instead of deprecated on_event
)

# CORS (Cross-Origin Resource Sharing) Configuration
# This allows the frontend to make requests to the API
# In production, restrict this to your actual frontend domain
# See: https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
    """
    Root endpoint - Basic health check.
    
    Returns:
        dict: Service information and status
    """
    return {
        "service": "CH Health OS API",
        "status": "healthy",
        "version": settings.API_VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    
    This endpoint is used by:
    - Render to check if the service is running
    - Monitoring tools to verify uptime
    - Load balancers to route traffic
    
    Returns:
        dict: Service health status
    """
    from app.core.database import test_connection
    
    # Test database connection
    db_connected = await test_connection()
    
    return {
        "status": "ok" if db_connected else "degraded",
        "environment": settings.ENVIRONMENT,
        "database": "connected" if db_connected else "disconnected",
    }


# =============================================================================
# Test Endpoints (Development Only)
# =============================================================================

from sqlalchemy import select
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models import User


@app.get("/api/test/users")
async def test_list_users(db: AsyncSession = Depends(get_db)):
    """
    Test endpoint - List all users.
    
    This demonstrates:
    - Database connection working
    - SQLAlchemy ORM working
    - Dependency injection working
    """
    stmt = select(User).limit(10)
    result = await db.execute(stmt)
    users = result.scalars().all()
    
    return {
        "status": "success",
        "orm": "SQLAlchemy 2.0",
        "count": len(users),
        "users": [
            {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
            }
            for user in users
        ]
    }


# =============================================================================
# API Routes
# =============================================================================

# Import and register API routers
# If there's an import error, it will be caught here
try:
    from app.api.routes import auth, users, routines, habits
    
    # Register all API routers
    # Each router has its own prefix, so we add /api here
    # Final paths will be: /api/auth/*, /api/users/*, /api/routines/*, /api/habits/*
    # Note: Auth router is empty (Supabase handles auth on frontend)
    app.include_router(auth.router, prefix="/api")
    app.include_router(users.router, prefix="/api")
    app.include_router(routines.router, prefix="/api")
    app.include_router(habits.router, prefix="/api")
    
    logger.info("api_routes_loaded", auth=True, users=True, routines=True, habits=True)
    print("✅ API routes loaded successfully!")
    print(f"   - Auth router: {len(auth.router.routes)} routes (Supabase Auth on frontend)")
    print(f"   - Users router: {len(users.router.routes)} routes")
    print(f"   - Routines router: {len(routines.router.routes)} routes")
    print(f"   - Habits router: {len(habits.router.routes)} routes")
except Exception as e:
    logger.error("api_routes_import_error", error=str(e), exc_info=True)
    print(f"❌ ERROR loading API routes: {e}")
    import traceback
    traceback.print_exc()
    # Re-raise to fail startup so we can see the error
    raise


if __name__ == "__main__":
    # This allows running the app with: python -m app.main
    # But in production, we use: uvicorn app.main:app
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,  # Auto-reload on code changes in development
    )
