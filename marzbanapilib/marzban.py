import httpx
from typing import Optional
from .utils import get_token_from_credentials
from .sections.user import UserAPI
from .sections.admin import AdminAPI
from .sections.system import SystemAPI
from .sections.core import CoreAPI
from .sections.node import NodeAPI


class MarzbanAPI:
    """
    Central client for interacting with Marzban VPN panel API.
    
    This class provides a unified interface to all API sections through
    modular sub-APIs for better organization and maintainability.
    
    You can authenticate in two ways:
    1. Using username and password (traditional method)
    2. Using a pre-existing access token (direct token method)
    
    Usage with username/password:
        async with MarzbanAPI("http://127.0.0.1:8000", "admin", "password") as api:
            users = await api.user.get_users()
            stats = await api.system.get_stats()
    
    Usage with access token:
        async with MarzbanAPI("http://127.0.0.1:8000", access_token="your_jwt_token") as api:
            users = await api.user.get_users()
            stats = await api.system.get_stats()
    """
    
    def __init__(
        self, 
        base_url: str, 
        username: Optional[str] = None, 
        password: Optional[str] = None,
        access_token: Optional[str] = None
    ):
        """
        Initialize MarzbanAPI client.
        
        Args:
            base_url: Base URL of Marzban API (e.g. http://127.0.0.1:8000)
            username: Admin username for authentication (optional if access_token provided)
            password: Admin password for authentication (optional if access_token provided)
            access_token: Pre-existing JWT token for direct authentication (optional)
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.access_token = access_token
        self.token: Optional[str] = None
        self.client = httpx.AsyncClient(timeout=30.0)
        
        # Initialize API sections (will be set after authentication)
        self.user: Optional[UserAPI] = None
        self.admin: Optional[AdminAPI] = None
        self.system: Optional[SystemAPI] = None
        self.core: Optional[CoreAPI] = None
        self.node: Optional[NodeAPI] = None
    
    async def __aenter__(self):
        """Async context manager entry - authenticate and initialize sections."""
        await self.authenticate()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - close the HTTP client."""
        await self.client.aclose()
    
    async def authenticate(self):
        """Authenticate with Marzban API and initialize all sections."""
        # Use provided access token or get new token from credentials
        if self.access_token:
            self.token = self.access_token
        else:
            if not self.username or not self.password:
                raise ValueError("Either access_token or both username and password must be provided")
            
            self.token = await get_token_from_credentials(
                self.username, 
                self.password, 
                self.base_url
            )
        
        # Initialize all API sections with shared client and token
        self.user = UserAPI(self.client, self.base_url, self.token)
        self.admin = AdminAPI(self.client, self.base_url, self.token)
        self.system = SystemAPI(self.client, self.base_url, self.token)
        self.core = CoreAPI(self.client, self.base_url, self.token)
        self.node = NodeAPI(self.client, self.base_url, self.token)
    
    async def close(self):
        """Close the HTTP client connection."""
        await self.client.aclose()
    
    # Backward compatibility methods (deprecated)
    # These methods are kept for backward compatibility but should not be used in new code
    
    async def get_system_stats(self):
        """
        DEPRECATED: Use api.system.get_stats() instead.
        Get system statistics.
        """
        if not self.system:
            raise ValueError("Not authenticated. Call authenticate() first.")
        return await self.system.get_stats()
    
    async def create_user(self, user_data):
        """
        DEPRECATED: Use api.user.create_user() instead.
        Create a new user.
        """
        if not self.user:
            raise ValueError("Not authenticated. Call authenticate() first.")
        return await self.user.create_user(user_data)
    
    async def get_user(self, username):
        """
        DEPRECATED: Use api.user.get_user() instead.
        Get user information.
        """
        if not self.user:
            raise ValueError("Not authenticated. Call authenticate() first.")
        return await self.user.get_user(username)
    
    async def delete_user(self, username):
        """
        DEPRECATED: Use api.user.delete_user() instead.
        Delete a user.
        """
        if not self.user:
            raise ValueError("Not authenticated. Call authenticate() first.")
        return await self.user.delete_user(username)
    
    async def restart_core(self):
        """
        DEPRECATED: Use api.core.restart() instead.
        Restart the Xray core.
        """
        if not self.core:
            raise ValueError("Not authenticated. Call authenticate() first.")
        return await self.core.restart()