import httpx
from typing import Dict, Any, List, Optional
from .base import BaseSection


class NodeAPI(BaseSection):
    """API section for node management operations."""
    
    async def get_all(self) -> List[Dict[str, Any]]:
        """
        Get list of all nodes.
        
        Returns:
            List of node dictionaries containing:
                - id, name, address, port, api_port
                - status, xray_version, message
                - created_at, last_status_change
                - uplink, downlink
                
        Raises:
            httpx.HTTPStatusError: If API request fails
        """
        headers = self._get_headers()
        
        response = await self.client.get(
            f"{self.base_url}/api/nodes",
            headers=headers
        )
        response.raise_for_status()
        
        return response.json()
    
    async def create(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new node.
        
        Args:
            node_data: Dictionary containing:
                - name: Node name (required)
                - address: Node address (required)
                - port: Node port (required)
                - api_port: Node API port (required)
                - usage_coefficient: Usage multiplier (optional, default 1.0)
                
        Returns:
            Dict with created node data
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If node already exists
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/node",
                headers=headers,
                json=node_data
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 409:
                raise ValueError(f"Node '{node_data.get('name')}' already exists") from e
            else:
                raise
    
    async def get(self, node_id: int) -> Dict[str, Any]:
        """
        Get node information by ID.
        
        Args:
            node_id: Node ID
            
        Returns:
            Dict with node data
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If node not found
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.get(
                f"{self.base_url}/api/node/{node_id}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Node with ID {node_id} not found") from e
            else:
                raise
    
    async def modify(self, node_id: int, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Modify an existing node.
        
        Args:
            node_id: Node ID
            node_data: Dictionary containing fields to update:
                - name: New node name (optional)
                - address: New address (optional)
                - port: New port (optional)
                - api_port: New API port (optional)
                - usage_coefficient: New usage multiplier (optional)
                - status: New status (optional)
                
        Returns:
            Dict with updated node data
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If node not found
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.put(
                f"{self.base_url}/api/node/{node_id}",
                headers=headers,
                json=node_data
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Node with ID {node_id} not found") from e
            else:
                raise
    
    async def delete(self, node_id: int) -> Dict[str, str]:
        """
        Delete a node.
        
        Args:
            node_id: Node ID
            
        Returns:
            Dict with success message
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If node not found
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.delete(
                f"{self.base_url}/api/node/{node_id}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Node with ID {node_id} not found") from e
            else:
                raise
    
    async def reconnect(self, node_id: int) -> Dict[str, str]:
        """
        Reconnect a node.
        
        Args:
            node_id: Node ID
            
        Returns:
            Dict with success message
            
        Raises:
            httpx.HTTPStatusError: If API request fails
            ValueError: If node not found
        """
        headers = self._get_headers()
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/node/{node_id}/reconnect",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Node with ID {node_id} not found") from e
            else:
                raise
    
    async def get_usage(self, start: Optional[str] = None, end: Optional[str] = None) -> Dict[str, Any]:
        """
        Get nodes usage statistics.
        
        Args:
            start: Start date in ISO format (optional)
            end: End date in ISO format (optional)
            
        Returns:
            Dict with:
                - usages: List of node usage records
                
        Raises:
            httpx.HTTPStatusError: If API request fails
        """
        headers = self._get_headers()
        params = {}
        
        if start:
            params["start"] = start
        if end:
            params["end"] = end
            
        response = await self.client.get(
            f"{self.base_url}/api/nodes/usage",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        
        return response.json()