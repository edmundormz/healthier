"""
FastAPI Dependencies

This module provides reusable dependencies for FastAPI routes.

Dependencies are functions that FastAPI calls automatically:
- Before route handler executes
- Can return values injected into route handler
- Can raise exceptions (which become HTTP errors)

Why dependencies?
- Reusable authentication logic
- Clean route handlers
- Easy to test (can override in tests)
- Follows DRY principle

See: https://fastapi.tiangolo.com/tutorial/dependencies/
"""

from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.supabase_auth import verify_supabase_jwt, get_user_id_from_token
from app.models import User
from app.services import UserService

# HTTPBearer handles Authorization header extraction
# Automatically looks for "Bearer <token>" in Authorization header
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from Supabase JWT token.
    
    This dependency:
    1. Extracts token from Authorization header
    2. Validates Supabase JWT token (signature, expiration, issuer)
    3. Extracts user ID from token ('sub' claim)
    4. Syncs user from auth.users to public.users if needed
    5. Fetches user from database
    6. Returns user (injected into route handler)
    
    Usage:
    ```python
    @router.get("/protected")
    async def protected_route(
        current_user: User = Depends(get_current_user)
    ):
        # current_user is automatically available
        return {"user_id": current_user.id}
    ```
    
    Args:
        credentials: HTTPBearer extracts token from Authorization header
        db: Database session (injected by FastAPI)
        
    Returns:
        Authenticated User object
        
    Raises:
        HTTPException 401: If token is invalid, expired, or missing
        HTTPException 404: If user not found (will sync from Supabase if needed)
        
    Security Notes:
    - Token must be valid Supabase JWT signed with RS256
    - Token must not be expired
    - Token issuer must match Supabase project URL
    - Token audience must be 'authenticated'
    """
    import structlog
    logger = structlog.get_logger()
    
    token = credentials.credentials
    logger.debug("auth_attempt", token_length=len(token) if token else 0)
    
    # Verify Supabase JWT token (async call)
    payload = await verify_supabase_jwt(token)
    if payload is None:
        logger.warning("jwt_verification_failed", reason="payload is None")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.debug("jwt_verified", user_id=payload.get("sub"))
    
    # Extract user ID from token (async call)
    # "sub" (subject) is the standard JWT claim for user identifier
    user_id = await get_user_id_from_token(token)
    if user_id is None:
        logger.warning("user_id_extraction_failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user identifier",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Fetch user from database
    service = UserService(db)
    user = await service.get_user_by_id(user_id)
    
    # If user doesn't exist in public.users, sync from Supabase auth.users
    if user is None:
        # Sync user from Supabase Auth
        user = await service.sync_user_from_supabase(user_id, payload)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    
    return user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Get current user if authenticated, None otherwise.
    
    This is useful for endpoints that work both with and without authentication.
    For example, public content that shows more details when logged in.
    
    Usage:
    ```python
    @router.get("/public")
    async def public_route(
        current_user: Optional[User] = Depends(get_current_user_optional)
    ):
        if current_user:
            return {"message": f"Hello {current_user.full_name}!"}
        return {"message": "Hello anonymous user!"}
    ```
    
    Args:
        credentials: Optional token (auto_error=False means no exception if missing)
        db: Database session
        
    Returns:
        User if authenticated, None otherwise
    """
    if credentials is None:
        return None
    
    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        # If token is invalid, just return None (not authenticated)
        return None
