"""
Database Connection and Session Management

This module sets up Supabase REST API client for database operations.

Why Direct REST API?
- Works reliably with Supabase's new secret key format
- Simple and straightforward HTTP requests
- Full control over authentication headers
- Compatible with all Supabase key types

We use httpx for async HTTP requests to Supabase's REST API.
See: https://supabase.com/docs/reference/rest/introduction
"""

from typing import Generator, Dict, Any, Optional
import httpx
import structlog

from app.core.config import settings

logger = structlog.get_logger()

# Supabase REST API base URL
SUPABASE_REST_URL = f"{settings.SUPABASE_URL}/rest/v1"

# HTTP client for Supabase API requests
# Using httpx for async HTTP operations
# See: https://www.python-httpx.org/
_client: Optional[httpx.AsyncClient] = None


def get_client() -> httpx.AsyncClient:
    """
    Get or create the HTTP client for Supabase API.
    
    Returns:
        httpx.AsyncClient: Async HTTP client configured for Supabase
    """
    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            base_url=SUPABASE_REST_URL,
            headers={
                "apikey": settings.SUPABASE_SECRET_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SECRET_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            },
            timeout=30.0,
        )
    return _client


class SupabaseClient:
    """
    Simple Supabase client wrapper using REST API.
    
    This provides a clean interface for database operations
    using Supabase's REST API with the secret key.
    """
    
    def __init__(self):
        self.client = get_client()
        self.base_url = SUPABASE_REST_URL
    
    def table(self, table_name: str) -> "TableBuilder":
        """
        Access a database table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            TableBuilder: Builder for table operations
        """
        return TableBuilder(self.client, table_name)


class TableBuilder:
    """Builder for table operations."""
    
    def __init__(self, client: httpx.AsyncClient, table_name: str):
        self.client = client
        self.table_name = table_name
        self._select = "*"
        self._filters: Dict[str, Any] = {}
        self._limit: Optional[int] = None
    
    def select(self, columns: str = "*") -> "TableBuilder":
        """
        Select columns to return.
        
        Args:
            columns: Column names (e.g., "id,name" or "*")
            
        Returns:
            TableBuilder: Self for chaining
        """
        self._select = columns
        return self
    
    def limit(self, count: int) -> "TableBuilder":
        """
        Limit number of rows returned.
        
        Args:
            count: Maximum number of rows
            
        Returns:
            TableBuilder: Self for chaining
        """
        self._limit = count
        return self
    
    async def execute(self) -> Dict[str, Any]:
        """
        Execute the query.
        
        Returns:
            Dict with 'data' and 'error' keys
        """
        url = f"/{self.table_name}"
        params = {"select": self._select}
        
        if self._limit:
            params["limit"] = str(self._limit)
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return {"data": response.json(), "error": None}
        except httpx.HTTPStatusError as e:
            logger.error("supabase_query_error", table=self.table_name, status=e.response.status_code)
            return {"data": None, "error": str(e)}
        except Exception as e:
            logger.error("supabase_query_exception", table=self.table_name, error=str(e))
            return {"data": None, "error": str(e)}


# Create global Supabase client instance
supabase = SupabaseClient()


def get_supabase() -> SupabaseClient:
    """
    Get the Supabase client instance.
    
    This is used as a FastAPI dependency:
    ```python
    @app.get("/users")
    async def get_users(db: SupabaseClient = Depends(get_supabase)):
        response = await db.table("users").select("*").execute()
        return response["data"]
    ```
    
    Returns:
        SupabaseClient: Supabase client instance
    """
    return supabase


def get_db() -> Generator[SupabaseClient, None, None]:
    """
    Dependency function that provides a Supabase client.
    
    Usage:
    ```python
    @app.get("/users")
    async def get_users(db: SupabaseClient = Depends(get_db)):
        response = await db.table("users").select("*").execute()
        return response["data"]
    ```
    
    Yields:
        SupabaseClient: Supabase client instance
    """
    yield supabase


async def test_connection() -> bool:
    """
    Test the database connection.
    
    This performs a simple query to verify the connection works.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        # Simple query to test connection
        response = await supabase.table("users").select("id").limit(1).execute()
        if response["error"]:
            logger.error("database_connection_test_failed", error=response["error"])
            return False
        logger.info("database_connection_test_successful")
        return True
    except Exception as e:
        logger.error("database_connection_test_failed", error=str(e))
        return False


async def init_db():
    """
    Initialize database (no-op for Supabase).
    
    Supabase uses migrations applied via SQL, not programmatic table creation.
    This function exists for compatibility but doesn't do anything.
    
    To create tables, use SQL migrations via Supabase dashboard or MCP.
    """
    logger.info("database_initialized", note="Using Supabase client - tables managed via migrations")


async def close_db():
    """
    Close database connections.
    
    Closes the HTTP client connection pool.
    """
    global _client
    if _client:
        await _client.aclose()
        _client = None
    logger.info("database_connections_closed")
