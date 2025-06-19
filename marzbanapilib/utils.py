import httpx
from typing import Optional


async def get_token_from_credentials(
    username: str, 
    password: str, 
    base_url: str
) -> str:
    """
    Get JWT token from Marzban API using admin credentials.
    
    Args:
        username: Admin username
        password: Admin password  
        base_url: Base URL of Marzban API (e.g. http://127.0.0.1:8000)
        
    Returns:
        JWT token string
        
    Raises:
        httpx.HTTPStatusError: If authentication fails
        httpx.RequestError: If connection fails
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{base_url}/api/admin/token",
                data={
                    "username": username,
                    "password": password
                }
            )
            response.raise_for_status()
            
            token_data = response.json()
            return token_data["access_token"]
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ValueError("Invalid credentials: username or password is incorrect") from e
            else:
                raise ValueError(f"Authentication failed with status {e.response.status_code}: {e.response.text}") from e
        except httpx.RequestError as e:
            raise ValueError(f"Failed to connect to Marzban API at {base_url}: {str(e)}") from e
        except KeyError:
            raise ValueError("Unexpected response format from Marzban API") 