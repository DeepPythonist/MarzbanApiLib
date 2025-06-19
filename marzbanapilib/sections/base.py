import httpx
from typing import Dict, Optional


class BaseSection:
    """Base class for all API sections."""
    
    def __init__(self, client: httpx.AsyncClient, base_url: str, token: Optional[str] = None):
        """
        Initialize base section with HTTP client and authentication.
        
        Args:
            client: Shared httpx AsyncClient instance
            base_url: Base URL of Marzban API
            token: JWT authentication token
        """
        self.client = client
        self.base_url = base_url
        self.token = token
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token."""
        if not self.token:
            raise ValueError("Not authenticated. Token is required.")
        
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }