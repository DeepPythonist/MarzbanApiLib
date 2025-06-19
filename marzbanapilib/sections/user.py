import httpx
from typing import Dict, Any, Optional, List
from .base import BaseSection


class UserAPI(BaseSection):
    """API section for user management operations."""
    
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new user in Marzban.
        
        Args:
            user_data: Dictionary containing user creation data:
                - username: str (3-32 chars, alphanumeric + underscore)
                - proxies: Dict of proxy configurations (e.g. {"vmess": {}, "vless": {}})
                - inbounds: Dict of inbound tags per protocol
                - expire: Optional[int] - Unix timestamp for expiration (0 for unlimited)
                - data_limit: Optional[int] - Data limit in bytes (0 for unlimited)
                - data_limit_reset_strategy: Optional[str] - "no_reset", "day", "week", "month"
                - status: Optional[str] - "active" or "on_hold"
                - note: Optional[str] - User note/description
                - on_hold_expire_duration: Optional[int] - Duration in seconds
                - on_hold_timeout: Optional[datetime] - When on_hold should start/end
                
        Returns:
            Dict containing created user data including:
                - username, status, used_traffic, lifetime_used_traffic
                - created_at, links, subscription_url, proxies
                - excluded_inbounds, expire, data_limit, etc.
                
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If user already exists (409 error)
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/user",
                headers=headers,
                json=user_data
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 409:
                raise ValueError(f"User '{user_data.get('username')}' already exists") from e
            elif e.response.status_code == 400:
                raise ValueError(f"Invalid user data: {e.response.text}") from e
            else:
                raise
    
    async def get_user(self, username: str) -> Dict[str, Any]:
        """
        Get user information by username.
        
        Args:
            username: Username of the user to retrieve
            
        Returns:
            Dict containing user data including:
                - username, status, used_traffic, lifetime_used_traffic
                - created_at, links, subscription_url, proxies
                - excluded_inbounds, expire, data_limit
                - admin info, note, online_at, etc.
                
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If user not found (404 error)
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.get(
                f"{self.base_url}/api/user/{username}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"User '{username}' not found") from e
            elif e.response.status_code == 403:
                raise ValueError(f"Access denied to user '{username}'") from e
            else:
                raise
    
    async def delete_user(self, username: str) -> Dict[str, str]:
        """
        Delete a user from Marzban.
        
        Args:
            username: Username of the user to delete
            
        Returns:
            Dict with success message {"detail": "User successfully deleted"}
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If user not found or access denied
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.delete(
                f"{self.base_url}/api/user/{username}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"User '{username}' not found") from e
            elif e.response.status_code == 403:
                raise ValueError(f"Access denied to delete user '{username}'") from e
            else:
                raise
    
    async def modify_user(self, username: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Modify an existing user.
        
        Args:
            username: Username of the user to modify
            user_data: Dictionary containing fields to update:
                - proxies: New proxy configurations (optional)
                - inbounds: New inbound configurations (optional)
                - expire: New expiration timestamp (optional)
                - data_limit: New data limit in bytes (optional)
                - data_limit_reset_strategy: New reset strategy (optional)
                - status: New status (optional)
                - note: New note (optional)
                - on_hold_expire_duration: New on-hold duration (optional)
                - on_hold_timeout: New on-hold timeout (optional)
                
        Returns:
            Dict with updated user data
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If user not found or invalid data
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.put(
                f"{self.base_url}/api/user/{username}",
                headers=headers,
                json=user_data
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                raise ValueError(f"Invalid user data: {e.response.text}") from e
            elif e.response.status_code == 403:
                raise ValueError(f"Access denied to modify user '{username}'") from e
            elif e.response.status_code == 404:
                raise ValueError(f"User '{username}' not found") from e
            else:
                raise
    
    async def get_users(self, offset: Optional[int] = None, limit: Optional[int] = None, 
                       username: Optional[List[str]] = None, search: Optional[str] = None,
                       admin: Optional[List[str]] = None, status: Optional[str] = None,
                       sort: Optional[str] = None) -> Dict[str, Any]:
        """
        Get list of users with filtering and pagination.
        
        Args:
            offset: Number of records to skip
            limit: Maximum number of records to return
            username: List of usernames to filter by
            search: Search term for username or note
            admin: List of admin usernames to filter by
            status: User status to filter by
            sort: Comma-separated sort options (e.g., "created_at,-username")
            
        Returns:
            Dict with:
                - users: List of user dictionaries
                - total: Total number of users matching criteria
                
        Raises:
            httpx.HTTPStatusError: If API request fails
        """
        headers = self._get_headers()
        params = {}
        
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        if username:
            params["username"] = username
        if search:
            params["search"] = search
        if admin:
            params["admin"] = admin
        if status:
            params["status"] = status
        if sort:
            params["sort"] = sort
            
        response = await self.client.get(
            f"{self.base_url}/api/users",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        
        return response.json()
    
    async def reset_data_usage(self, username: str) -> Dict[str, Any]:
        """
        Reset user's data usage to zero.
        
        Args:
            username: Username of the user
            
        Returns:
            Dict with updated user data
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If user not found or access denied
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/user/{username}/reset",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                raise ValueError(f"Access denied to reset user '{username}'") from e
            elif e.response.status_code == 404:
                raise ValueError(f"User '{username}' not found") from e
            else:
                raise
    
    async def revoke_subscription(self, username: str) -> Dict[str, Any]:
        """
        Revoke user's subscription (invalidates subscription link).
        
        Args:
            username: Username of the user
            
        Returns:
            Dict with updated user data
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If user not found or access denied
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/user/{username}/revoke_sub",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                raise ValueError(f"Access denied to revoke subscription for user '{username}'") from e
            elif e.response.status_code == 404:
                raise ValueError(f"User '{username}' not found") from e
            else:
                raise
    
    async def get_usage(self, username: str, start: Optional[str] = None, end: Optional[str] = None) -> Dict[str, Any]:
        """
        Get user's usage statistics.
        
        Args:
            username: Username of the user
            start: Start date in ISO format (optional)
            end: End date in ISO format (optional)
            
        Returns:
            Dict with:
                - username: Username
                - usages: List of usage records by node
                
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If user not found or access denied
        """
        headers = self._get_headers()
        params = {}
        
        if start:
            params["start"] = start
        if end:
            params["end"] = end
            
        try:
            response = await self.client.get(
                f"{self.base_url}/api/user/{username}/usage",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                raise ValueError(f"Access denied to view usage for user '{username}'") from e
            elif e.response.status_code == 404:
                raise ValueError(f"User '{username}' not found") from e
            else:
                raise
    
    async def activate_next_plan(self, username: str) -> Dict[str, Any]:
        """
        Activate user's next plan.
        
        Args:
            username: Username of the user
            
        Returns:
            Dict with updated user data
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If user not found or doesn't have next plan
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/user/{username}/active-next",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                raise ValueError(f"Access denied to activate next plan for user '{username}'") from e
            elif e.response.status_code == 404:
                raise ValueError(f"User '{username}' not found or doesn't have next plan") from e
            else:
                raise
    
    async def reset_all_users_data_usage(self) -> Dict[str, str]:
        """
        Reset all users' data usage (requires sudo privileges).
        
        Returns:
            Dict with success message
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If access denied
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/users/reset",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                raise ValueError("Access denied. Resetting all users requires sudo privileges") from e
            else:
                raise
    
    async def set_owner(self, username: str, admin_username: str) -> Dict[str, Any]:
        """
        Set a new owner (admin) for a user.
        
        Args:
            username: Username of the user
            admin_username: Username of the new admin owner
            
        Returns:
            Dict with updated user data
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If user or admin not found
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.put(
                f"{self.base_url}/api/user/{username}/set-owner",
                headers=headers,
                params={"admin_username": admin_username}
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError("User or admin not found") from e
            else:
                raise
    
    async def get_expired_users(self, expired_after: Optional[str] = None, expired_before: Optional[str] = None) -> List[str]:
        """
        Get list of expired users.
        
        Args:
            expired_after: Filter users expired after this date (ISO format)
            expired_before: Filter users expired before this date (ISO format)
            
        Returns:
            List of usernames of expired users
            
        Raises:
            httpx.HTTPStatusError: If API request fails
        """
        headers = self._get_headers()
        params = {}
        
        if expired_after:
            params["expired_after"] = expired_after
        if expired_before:
            params["expired_before"] = expired_before
            
        response = await self.client.get(
            f"{self.base_url}/api/users/expired",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        
        return response.json()
    
    async def delete_expired_users(self, expired_after: Optional[str] = None, expired_before: Optional[str] = None) -> List[str]:
        """
        Delete expired users.
        
        Args:
            expired_after: Delete users expired after this date (ISO format)
            expired_before: Delete users expired before this date (ISO format)
            
        Returns:
            List of usernames of deleted users
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If no expired users found
        """
        headers = self._get_headers()
        params = {}
        
        if expired_after:
            params["expired_after"] = expired_after
        if expired_before:
            params["expired_before"] = expired_before
            
        try:
            response = await self.client.delete(
                f"{self.base_url}/api/users/expired",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError("No expired users found in the specified date range") from e
            else:
                raise
    
    async def get_all_usage(self, start: Optional[str] = None, end: Optional[str] = None, admin: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get usage statistics for all users.
        
        Args:
            start: Start date in ISO format (optional)
            end: End date in ISO format (optional)
            admin: List of admin usernames to filter by (optional)
            
        Returns:
            Dict with:
                - usages: List of usage records
                
        Raises:
            httpx.HTTPStatusError: If API request fails
        """
        headers = self._get_headers()
        params = {}
        
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        if admin:
            params["admin"] = admin
            
        response = await self.client.get(
            f"{self.base_url}/api/users/usage",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        
        return response.json() 