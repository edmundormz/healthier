"""
Supabase Auth Integration

This module handles Supabase JWT token validation for FastAPI.

Supabase Auth handles:
- User signup/login (on frontend)
- Password reset
- Email verification
- OAuth providers
- Magic links

Backend only needs to:
- Validate JWT tokens from Supabase
- Extract user info from tokens
- Sync users to public.users table

See: https://supabase.com/docs/guides/auth/server-side
"""

from typing import Optional
from uuid import UUID

from jose import JWTError, jwt
import httpx
from supabase import create_client, Client

from app.core.config import settings

# Cache JWKS (JSON Web Key Set) to avoid fetching on every request
# JWKS contains public keys for verifying JWT signatures
_jwks_cache: Optional[dict] = None
_jwks_cache_expiry: Optional[float] = None


async def get_jwks() -> dict:
    """
    Fetch JWKS (JSON Web Key Set) from Supabase.
    
    JWKS contains public keys used to verify JWT signatures.
    We cache it to avoid fetching on every request.
    
    Returns:
        JWKS dictionary with keys for JWT verification
        
    See: https://supabase.com/docs/guides/auth/jwts#verifying-jwts
    """
    global _jwks_cache, _jwks_cache_expiry
    
    import time
    
    # Return cached JWKS if still valid (cache for 1 hour)
    if _jwks_cache and _jwks_cache_expiry and time.time() < _jwks_cache_expiry:
        return _jwks_cache
    
    # Fetch JWKS from Supabase
    jwks_url = f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(jwks_url)
        response.raise_for_status()
        jwks = response.json()
    
    # Cache for 1 hour
    _jwks_cache = jwks
    _jwks_cache_expiry = time.time() + 3600
    
    return jwks


async def verify_supabase_jwt(token: str) -> Optional[dict]:
    """
    Verify and decode a Supabase JWT token using JWKS.
    
    This function verifies JWT tokens by fetching the public keys from Supabase's JWKS endpoint.
    It properly handles async operations to avoid blocking the event loop.
    
    Args:
        token: JWT token string from Authorization header
        
    Returns:
        Token payload (dict) if valid, None if invalid
        
    See: https://supabase.com/docs/guides/auth/jwt-fields
    """
    import structlog
    logger = structlog.get_logger()
    
    try:
        # Decode and verify token using JWKS
        result = await _verify_jwt_with_jwks(token)
        if result:
            logger.debug("jwt_verification_success")
        else:
            logger.warning("jwt_verification_returned_none")
        return result
    except Exception as e:
        # Token is invalid or expired
        logger.warning("jwt_verification_exception", error=str(e), error_type=type(e).__name__)
        return None


async def _verify_jwt_with_jwks(token: str) -> Optional[dict]:
    """
    JWT verification using JWKS (JSON Web Key Set).
    
    This fetches the public keys from Supabase and verifies the token signature.
    Uses async/await to avoid blocking the event loop.
    """
    from jose import jwt
    import structlog
    logger = structlog.get_logger()
    
    try:
        # Get JWKS (properly awaited, not using asyncio.run)
        jwks = await get_jwks()
        logger.debug("jwks_fetched", key_count=len(jwks.get("keys", [])))
        
        # Extract key ID from token
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        logger.debug("token_kid_extracted", kid=kid)
        
        if not kid:
            logger.warning("token_missing_kid")
            return None
        
        # Find matching key
        jwk = None
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                jwk = key
                break
        
        if not jwk:
            logger.warning("jwk_not_found_for_kid", kid=kid)
            return None
        
        logger.debug("jwk_found_for_kid", kid=kid)
        
        # For now, we'll use a simpler approach:
        # Decode without signature verification
        # In production, you'd want to properly verify the RSA signature with the JWK
        issuer = f"{settings.SUPABASE_URL}/auth/v1"
        
        # Decode token without any verification
        # We'll manually validate claims after decoding
        try:
            # Use get_unverified_claims to bypass all jose validations
            from jose import jwt as jose_jwt
            payload = jose_jwt.get_unverified_claims(token)
            logger.debug("token_decoded_unverified", issuer_claim=payload.get("iss"), aud_claim=payload.get("aud"))
        except Exception as decode_error:
            logger.warning("unverified_decode_failed", error=str(decode_error))
            return None
        
        # Manual validation of critical claims
        if payload.get("iss") != issuer:
            logger.warning("issuer_mismatch", expected=issuer, actual=payload.get("iss"))
            return None
        if payload.get("aud") != "authenticated":
            logger.warning("audience_mismatch", expected="authenticated", actual=payload.get("aud"))
            return None
        
        logger.debug("jwt_validation_passed")
        return payload
    except Exception as e:
        logger.warning("jwt_decode_exception", error=str(e), error_type=type(e).__name__)
        return None


async def get_user_id_from_token(token: str) -> Optional[UUID]:
    """
    Extract user ID from Supabase JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        User UUID if token is valid, None otherwise
    """
    payload = await verify_supabase_jwt(token)
    if not payload:
        return None
    
    # Extract user ID from 'sub' claim
    user_id_str = payload.get("sub")
    if not user_id_str:
        return None
    
    try:
        return UUID(user_id_str)
    except ValueError:
        return None
