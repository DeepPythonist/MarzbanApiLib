import httpx
from typing import Dict, Any, Optional, List
from .base import BaseSection


class AdminAPI(BaseSection):
    """API section for admin management operations."""
    
    async def get_current(self) -> Dict[str, Any]:
        """
        Get current authenticated admin information.
        
        Returns:
            Dict containing admin info:
                - username: Admin username
                - is_sudo: Whether admin has sudo privileges
                - telegram_id: Optional Telegram ID
                - discord_webhook: Optional Discord webhook URL
                - users_usage: Total usage by admin's users
                
        Raises:
            httpx.HTTPStatusError: If API request fails
        """
        headers = self._get_headers()
        
        response = await self.client.get(
            f"{self.base_url}/api/admin",
            headers=headers
        )
        response.raise_for_status()
        
        return response.json()
    
    async def create(self, admin_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new admin (requires sudo privileges).
        
        Args:
            admin_data: Dictionary containing:
                - username: Admin username (required)
                - password: Admin password (required)
                - is_sudo: Whether to grant sudo privileges (required)
                - telegram_id: Optional Telegram ID
                - discord_webhook: Optional Discord webhook URL
                
        Returns:
            Dict with created admin data
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If admin already exists or access denied
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/admin",
                headers=headers,
                json=admin_data
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                raise ValueError("Access denied. Creating admins requires sudo privileges") from e
            elif e.response.status_code == 409:
                raise ValueError(f"Admin '{admin_data.get('username')}' already exists") from e
            else:
                raise
    
    async def modify(self, username: str, admin_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Modify an existing admin (requires sudo privileges).
        
        Args:
            username: Username of admin to modify
            admin_data: Dictionary containing fields to update:
                - password: New password (optional)
                - is_sudo: Whether to grant sudo privileges
                - telegram_id: Telegram ID (optional)
                - discord_webhook: Discord webhook URL (optional)
                
        Returns:
            Dict with updated admin data
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If access denied
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.put(
                f"{self.base_url}/api/admin/{username}",
                headers=headers,
                json=admin_data
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                raise ValueError("Access denied. Modifying admins requires sudo privileges") from e
            else:
                raise
    
    async def delete(self, username: str) -> Dict[str, str]:
        """
        Delete an admin (requires sudo privileges).
        
        Args:
            username: Username of admin to delete
            
        Returns:
            Dict with success message
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If trying to delete sudo admin or access denied
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.delete(
                f"{self.base_url}/api/admin/{username}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                raise ValueError("Access denied. Cannot delete sudo admins or requires sudo privileges") from e
            else:
                raise
    
    async def get_all(self, offset: Optional[int] = None, limit: Optional[int] = None, username: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get list of all admins (requires sudo privileges).
        
        Args:
            offset: Number of records to skip
            limit: Maximum number of records to return
            username: Filter by username (optional)
            
        Returns:
            List of admin dictionaries
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If access denied
        """
        headers = self._get_headers()
        params = {}
        
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        if username is not None:
            params["username"] = username
            
        try:
            response = await self.client.get(
                f"{self.base_url}/api/admins",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                raise ValueError("Access denied. Listing admins requires sudo privileges") from e
            else:
                raise 