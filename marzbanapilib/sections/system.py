import httpx
from typing import Dict, Any, List, Optional
from .base import BaseSection


class SystemAPI(BaseSection):
    """API section for system statistics and configuration."""
    
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get system statistics including CPU, memory, bandwidth and user counts.
        
        Returns:
            Dict containing system statistics:
            - version: Marzban version
            - mem_total: Total memory in bytes
            - mem_used: Used memory in bytes
            - cpu_cores: Number of CPU cores
            - cpu_usage: CPU usage percentage
            - total_user: Total number of users
            - online_users: Number of online users
            - users_active: Number of active users
            - users_disabled: Number of disabled users
            - users_expired: Number of expired users
            - users_limited: Number of limited users
            - users_on_hold: Number of on-hold users
            - incoming_bandwidth: Total incoming bandwidth
            - outgoing_bandwidth: Total outgoing bandwidth
            - incoming_bandwidth_speed: Current incoming speed
            - outgoing_bandwidth_speed: Current outgoing speed
            
        Raises:
            httpx.HTTPStatusError: If API request fails
        """
        headers = self._get_headers()
        
        response = await self.client.get(
            f"{self.base_url}/api/system",
            headers=headers
        )
        response.raise_for_status()
        
        return response.json()
    
    async def get_inbounds(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get inbound configurations grouped by protocol.
        
        Returns:
            Dict with protocol names as keys and lists of inbound configs as values
            
        Raises:
            httpx.HTTPStatusError: If API request fails
        """
        headers = self._get_headers()
        
        response = await self.client.get(
            f"{self.base_url}/api/inbounds",
            headers=headers
        )
        response.raise_for_status()
        
        return response.json()
    
    async def get_hosts(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get proxy hosts grouped by inbound tag (requires sudo privileges).
        
        Returns:
            Dict with inbound tags as keys and lists of hosts as values
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If access denied
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.get(
                f"{self.base_url}/api/hosts",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                raise ValueError("Access denied. Getting hosts requires sudo privileges") from e
            else:
                raise
    
    async def modify_hosts(self, hosts_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Modify proxy hosts (requires sudo privileges).
        
        Args:
            hosts_data: Dict with inbound tags as keys and lists of host configs as values
            
        Returns:
            Dict with updated hosts grouped by inbound tag
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If invalid inbound tag or access denied
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.put(
                f"{self.base_url}/api/hosts",
                headers=headers,
                json=hosts_data
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                raise ValueError(f"Invalid hosts data: {e.response.text}") from e
            elif e.response.status_code == 403:
                raise ValueError("Access denied. Modifying hosts requires sudo privileges") from e
            else:
                raise 