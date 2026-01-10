"""
Application Configuration

This module handles all environment variables and application settings.
It uses Pydantic Settings for validation and type safety.

Why Pydantic Settings?
- Automatic validation of environment variables
- Type hints help catch errors early
- Clear error messages if required vars are missing
- Easy to test (can override in tests)

See: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings are loaded from .env file or environment variables.
    Pydantic will validate types and required fields automatically.
    """

    # Supabase Configuration
    # New key system (publishable + secret keys)
    # See: https://supabase.com/docs/guides/api/api-keys
    SUPABASE_URL: str
    SUPABASE_PUBLISHABLE_KEY: str  # Replaces anon key (safe for frontend)
    SUPABASE_SECRET_KEY: str  # Replaces service_role key (backend only)

    # Telegram Bot
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_WEBHOOK_SECRET: str

    # OpenAI (for LangGraph/Vita)
    OPENAI_API_KEY: str

    # Application Settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    TIMEZONE: str = "America/Chicago"

    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_TITLE: str = "CH Health OS API"
    API_VERSION: str = "0.1.0"

    # CORS - can be comma-separated string or list
    CORS_ORIGINS: List[str] | str = ["http://localhost:3000", "http://localhost:8000"]

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Logging
    LOG_LEVEL: str = "INFO"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | List[str]) -> List[str]:
        """
        Convert comma-separated string to list.
        
        This allows CORS_ORIGINS to be set as:
        - String: "http://localhost:3000,http://localhost:8000"
        - List: ["http://localhost:3000", "http://localhost:8000"]
        
        Args:
            v: CORS origins as string or list
            
        Returns:
            List of origin URLs
        """
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # Pydantic v2 configuration
    # This tells Pydantic to load from .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,  # Environment variable names must match exactly
    )


# Create a single instance of settings
# This is imported throughout the application
# It's created once at startup and reused everywhere
settings = Settings()


# Validate critical settings at import time
# This ensures the app won't start if something is wrong
def validate_settings():
    """
    Validate that critical settings are properly configured.
    
    This catches configuration errors at startup rather than
    during runtime when a feature is first used.
    """
    if settings.ENVIRONMENT == "production" and settings.DEBUG:
        raise ValueError("DEBUG must be False in production")

    if settings.ENVIRONMENT == "production" and "localhost" in " ".join(
        settings.CORS_ORIGINS
    ):
        raise ValueError("Remove localhost from CORS_ORIGINS in production")

    # Validate Supabase URL format
    if not settings.SUPABASE_URL.startswith("https://"):
        raise ValueError("SUPABASE_URL must start with https://")


# Run validation on import
validate_settings()
