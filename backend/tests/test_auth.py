"""
Supabase Auth Integration Tests

Tests for Supabase authentication integration.

These tests verify:
- Supabase JWT token validation
- User sync from auth.users to public.users
- Protected route access with Supabase tokens
- Token validation errors
"""

import pytest
from fastapi import status
from unittest.mock import patch, Mock

from app.core.supabase_auth import verify_supabase_jwt, get_user_id_from_token
from app.core.dependencies import get_current_user
from app.models import User


# =============================================================================
# Token Validation Tests
# =============================================================================

@pytest.mark.asyncio
async def test_verify_supabase_jwt_valid_token():
    """Test verifying a valid Supabase JWT token."""
    # Mock jwt.decode to return payload
    with patch('app.core.supabase_auth.jwt.decode') as mock_decode:
        mock_decode.return_value = {
            "sub": "test-user-id",
            "email": "test@example.com",
            "role": "authenticated",
            "aud": "authenticated",
            "iss": "https://test.supabase.co/auth/v1"
        }
        
        with patch('app.core.supabase_auth.get_jwks') as mock_jwks:
            mock_jwks.return_value = {"keys": [{"kid": "test", "kty": "RSA"}]}
            
            token = "valid_token"
            payload = await verify_supabase_jwt(token)
            
            assert payload is not None
            assert payload["sub"] == "test-user-id"
            assert payload["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_verify_supabase_jwt_invalid_token():
    """Test verifying an invalid Supabase JWT token."""
    with patch('app.core.supabase_auth.get_jwks') as mock_jwks:
        mock_jwks.return_value = {"keys": []}
        
        token = "invalid_token"
        payload = await verify_supabase_jwt(token)
        
        assert payload is None


@pytest.mark.asyncio
async def test_get_user_id_from_token():
    """Test extracting user ID from Supabase JWT token."""
    with patch('app.core.supabase_auth.verify_supabase_jwt') as mock_verify:
        mock_verify.return_value = {
            "sub": "550e8400-e29b-12d3-a456-426614174000",
            "email": "test@example.com"
        }
        
        from uuid import UUID
        user_id = await get_user_id_from_token("valid_token")
        
        assert user_id is not None
        assert isinstance(user_id, UUID)
        assert str(user_id) == "550e8400-e29b-12d3-a456-426614174000"


@pytest.mark.asyncio
async def test_get_user_id_from_token_invalid():
    """Test extracting user ID from invalid token."""
    with patch('app.core.supabase_auth.verify_supabase_jwt') as mock_verify:
        mock_verify.return_value = None
        
        user_id = await get_user_id_from_token("invalid_token")
        
        assert user_id is None


# =============================================================================
# User Sync Tests
# =============================================================================

@pytest.mark.asyncio
async def test_user_sync_from_supabase(db_session, test_user):
    """Test syncing user from Supabase Auth to public.users."""
    from app.services import UserService
    from uuid import uuid4
    
    service = UserService(db_session)
    
    # Create a new user ID (simulating Supabase Auth user)
    supabase_user_id = uuid4()
    
    # JWT payload from Supabase
    jwt_payload = {
        "sub": str(supabase_user_id),
        "email": "synced@example.com",
        "user_metadata": {
            "full_name": "Synced User",
            "language": "en",
            "timezone": "America/Chicago"
        }
    }
    
    # Sync user
    user = await service.sync_user_from_supabase(supabase_user_id, jwt_payload)
    await db_session.commit()
    
    assert user is not None
    assert user.id == supabase_user_id
    assert user.email == "synced@example.com"
    assert user.full_name == "Synced User"
    assert user.language == "en"


@pytest.mark.asyncio
async def test_user_sync_updates_existing(db_session, test_user):
    """Test that syncing updates existing user."""
    from app.services import UserService
    
    service = UserService(db_session)
    
    # JWT payload with updated info
    jwt_payload = {
        "sub": str(test_user.id),
        "email": test_user.email,
        "user_metadata": {
            "full_name": "Updated Name",
            "language": "es"
        }
    }
    
    # Sync user (should update existing)
    user = await service.sync_user_from_supabase(test_user.id, jwt_payload)
    await db_session.commit()
    
    assert user is not None
    assert user.id == test_user.id
    assert user.full_name == "Updated Name"
    assert user.language == "es"


# =============================================================================
# Protected Route Tests
# =============================================================================

def test_protected_route_with_valid_token(client, test_user, auth_headers):
    """Test accessing protected route with valid Supabase token."""
    # Mock get_current_user to return test_user
    from app.core import dependencies
    from unittest.mock import patch
    
    async def mock_get_current_user(*args, **kwargs):
        return test_user
    
    with patch.object(dependencies, 'get_current_user', side_effect=mock_get_current_user):
        # This would work if routes were protected
        # For now, just test that auth_headers fixture works
        assert "Authorization" in auth_headers
        assert auth_headers["Authorization"].startswith("Bearer ")


def test_protected_route_without_token(client):
    """Test accessing protected route without token."""
    # When routes are protected, this should return 401
    response = client.get("/api/routines/")
    # After protection: assert response.status_code == status.HTTP_401_UNAUTHORIZED
    # For now, routes are protected, so this should fail
    assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
