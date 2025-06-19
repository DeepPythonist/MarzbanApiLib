import httpx
from typing import Dict, Any
from .base import BaseSection


class CoreAPI(BaseSection):
    """API section for Xray core management."""
    
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get Xray core statistics.
        
        Returns:
            Dict with:
                - version: Xray version
                - started: Core start timestamp
                - logs_websocket: WebSocket endpoint for logs
                
        Raises:
            httpx.HTTPStatusError: If API request fails
        """
        headers = self._get_headers()
        
        response = await self.client.get(
            f"{self.base_url}/api/core",
            headers=headers
        )
        response.raise_for_status()
        
        return response.json()
    
    async def restart(self) -> Dict[str, Any]:
        """
        Restart the Xray core and all connected nodes.
        
        Note: This operation requires sudo admin privileges.
        
        Returns:
            Empty dict {} on success
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If not authorized (requires sudo admin)
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/core/restart",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                raise ValueError("Access denied. This operation requires sudo admin privileges") from e
            else:
                raise
    
    async def get_config(self) -> Dict[str, Any]:
        """
        Get current Xray core configuration (requires sudo privileges).
        
        Returns:
            Dict with complete Xray configuration
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If access denied
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.get(
                f"{self.base_url}/api/core/config",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                raise ValueError("Access denied. Getting core config requires sudo privileges") from e
            else:
                raise
    
    async def modify_config(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Modify Xray core configuration (requires sudo privileges).
        
        Args:
            config_data: Complete Xray configuration dictionary
            
        Returns:
            Dict with updated configuration
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If invalid config or access denied
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.put(
                f"{self.base_url}/api/core/config",
                headers=headers,
                json=config_data
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                raise ValueError(f"Invalid core configuration: {e.response.text}") from e
            elif e.response.status_code == 403:
                raise ValueError("Access denied. Modifying core config requires sudo privileges") from e
            else:
                raise 