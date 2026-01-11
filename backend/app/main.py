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
    )
    
    yield  # Application runs here
    
    # Shutdown code (runs when app stops)
    # Good place to:
    # - Close database connections
    # - Cleanup resources
    # - Save state if needed
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
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
    }


# Future route imports will go here
# Example:
# from app.api.routes import routines, habits, telegram
# app.include_router(routines.router, prefix="/api/routines", tags=["routines"])
# app.include_router(habits.router, prefix="/api/habits", tags=["habits"])
# app.include_router(telegram.router, prefix="/api/telegram", tags=["telegram"])


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
