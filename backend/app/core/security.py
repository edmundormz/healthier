"""
Security Utilities

This module handles:
- Password hashing and verification (bcrypt)

⚠️ LEGACY JWT FUNCTIONS (NOT USED):
- create_access_token() and decode_access_token() are NOT used
- This project uses Supabase Auth for JWT token validation
- Supabase validates tokens using their own public keys (JWKS)
- These functions are kept for potential future use or reference

Why bcrypt?
- Industry standard for password hashing
- Automatically handles salting
- Slow by design (prevents brute force attacks)
- See: https://en.wikipedia.org/wiki/Bcrypt

Security Best Practices:
- Never store plain text passwords
- Always hash passwords before storing
- Validate tokens on every request (using Supabase Auth)
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing context
# bcrypt is the default algorithm (secure and widely used)
# rounds=12 means 2^12 = 4096 iterations (good balance of security/speed)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    This function:
    1. Takes a plain text password
    2. Generates a random salt
    3. Hashes password + salt
    4. Returns the hashed password (includes salt)
    
    Why hash passwords?
    - If database is compromised, attackers can't see real passwords
    - Each password gets unique salt (prevents rainbow table attacks)
    - bcrypt is slow by design (prevents brute force)
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password (can be stored in database)
        
    Example:
    ```python
    hashed = hash_password("my_secret_password")
    # Store 'hashed' in database, never store plain password
    ```
    
    See: https://passlib.readthedocs.io/en/stable/lib/passlib.context.html
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    
    This function:
    1. Takes plain password and stored hash
    2. Extracts salt from hash
    3. Hashes plain password with same salt
    4. Compares results
    
    Args:
        plain_password: Password to verify (from user input)
        hashed_password: Stored hash (from database)
        
    Returns:
        True if password matches, False otherwise
        
    Example:
    ```python
    if verify_password("my_password", user.hashed_password):
        print("Login successful!")
    ```
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    ⚠️ LEGACY FUNCTION - NOT USED
    
    This function is NOT used in the current application.
    We use Supabase Auth for JWT token generation and validation.
    
    Kept for reference or potential future use.
    
    Create a JWT access token.
    
    JWT tokens contain:
    - "sub" (subject): User ID or email
    - "exp" (expiration): When token expires
    - Custom claims: Any other data you want
    
    Token structure:
    - Header: Algorithm and token type
    - Payload: Data (user info, expiration)
    - Signature: Ensures token wasn't tampered with
    
    Args:
        data: Dictionary of claims to include in token
            Must include "sub" (subject/user identifier)
        expires_delta: Optional custom expiration time
            
    Returns:
        Encoded JWT token string
        
    See: https://python-jose.readthedocs.io/en/latest/jwt/api.html
    """
    raise NotImplementedError(
        "This function is not used. Use Supabase Auth for JWT token generation."
    )


def decode_access_token(token: str) -> Optional[dict]:
    """
    ⚠️ LEGACY FUNCTION - NOT USED
    
    This function is NOT used in the current application.
    We use Supabase Auth for JWT token validation (see supabase_auth.py).
    
    Kept for reference or potential future use.
    
    Decode and validate a JWT access token.
    
    Args:
        token: JWT token string (from Authorization header)
        
    Returns:
        Token payload (dict with user info) if valid, None if invalid
        
    Security Notes:
    - Use verify_supabase_jwt() from supabase_auth.py instead
    - Supabase validates tokens using their own public keys (JWKS)
    """
    raise NotImplementedError(
        "This function is not used. Use verify_supabase_jwt() from supabase_auth.py instead."
    )
