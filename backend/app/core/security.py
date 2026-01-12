"""
Security Utilities

This module handles:
- Password hashing and verification (bcrypt)
- JWT token generation and validation
- Token expiration and refresh logic

Why bcrypt?
- Industry standard for password hashing
- Automatically handles salting
- Slow by design (prevents brute force attacks)
- See: https://en.wikipedia.org/wiki/Bcrypt

Why JWT?
- Stateless authentication (no server-side sessions)
- Can include user info in token
- Works well with microservices
- See: https://jwt.io/introduction

Security Best Practices:
- Never store plain text passwords
- Always hash passwords before storing
- Use strong secret keys (32+ characters)
- Set reasonable token expiration times
- Validate tokens on every request
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
            If None, uses ACCESS_TOKEN_EXPIRE_MINUTES from settings
            
    Returns:
        Encoded JWT token string
        
    Example:
    ```python
    token = create_access_token(
        data={"sub": "user@example.com", "user_id": str(user.id)}
    )
    # Client sends this token in Authorization header
    ```
    
    See: https://python-jose.readthedocs.io/en/latest/jwt/api.html
    """
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # Add expiration to token
    to_encode.update({"exp": expire})
    
    # Encode token with secret key
    # SECRET_KEY must be kept secret (never commit to git!)
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT access token.
    
    This function:
    1. Decodes the token
    2. Verifies signature (ensures token wasn't tampered)
    3. Checks expiration
    4. Returns payload if valid
    
    Args:
        token: JWT token string (from Authorization header)
        
    Returns:
        Token payload (dict with user info) if valid, None if invalid
        
    Raises:
        JWTError: If token is invalid, expired, or tampered with
        
    Example:
    ```python
    payload = decode_access_token(token)
    if payload:
        user_id = payload.get("sub")
        print(f"Authenticated user: {user_id}")
    ```
    
    Security Notes:
    - Always validate tokens on every request
    - Never trust client data without verification
    - Expired tokens are automatically rejected
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        # Token is invalid, expired, or tampered with
        return None
