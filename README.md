# MarzbanAPILib

A modern, async Python client library for interacting with [Marzban VPN panel](https://github.com/Gozargah/Marzban) API.

## Features

- 🚀 **Async/await support** - Built with modern Python async patterns
- 📦 **Modular design** - Organized into logical sections for better maintainability  
- 🔐 **Type hints** - Full type annotation for better IDE support
- ⚡ **Simple & intuitive** - Easy to use API interface
- 🛡️ **Error handling** - Comprehensive error handling with meaningful messages
- 📚 **Well documented** - Detailed documentation for all methods

## Installation

Install using pip:

```bash
pip install marzbanapilib
```

## Quick Start

### Authentication with Username/Password

```python
import asyncio
from marzbanapilib import MarzbanAPI

async def main():
    # Create API client using username and password
    async with MarzbanAPI(
        base_url="http://127.0.0.1:8000",
        username="admin", 
        password="password"
    ) as api:
        # Get system statistics
        stats = await api.system.get_stats()
        print(f"Total users: {stats['total_user']}")
        
        # Create a new user
        user = await api.user.create_user({
            "username": "test_user",
            "proxies": {"vmess": {}, "vless": {}},
            "expire": 0,  # No expiration
            "data_limit": 0  # Unlimited
        })
        print(f"Created user: {user['username']}")

# Run the async function
asyncio.run(main())
```

### Authentication with Access Token

```python
import asyncio
from marzbanapilib import MarzbanAPI

async def main():
    # Use pre-existing access token (no username/password needed)
    async with MarzbanAPI(
        base_url="http://127.0.0.1:8000",
        access_token="your_jwt_token_here"
    ) as api:
        # Get system statistics
        stats = await api.system.get_stats()
        print(f"Total users: {stats['total_user']}")

asyncio.run(main())
```

## Architecture

The library is organized into modular sections:

- **`user`** - User management operations
- **`admin`** - Admin management operations  
- **`system`** - System statistics and configuration
- **`core`** - Xray core management
- **`node`** - Multi-node management

### Using Sections

```python
async with MarzbanAPI(...) as api:
    # User operations
    await api.user.create_user(...)
    await api.user.get_users()
    await api.user.reset_data_usage("username")
    
    # System operations
    await api.system.get_stats()
    await api.system.get_inbounds()
    
    # Core operations
    await api.core.restart()
    await api.core.get_config()
    
    # Node operations
    await api.node.get_all()
    await api.node.create(...)
```

## Advanced Usage

### Manual Authentication

```python
# With username/password
api = MarzbanAPI("http://127.0.0.1:8000", "admin", "password")
await api.authenticate()

# Or with access token
api = MarzbanAPI("http://127.0.0.1:8000", access_token="your_jwt_token")
await api.authenticate()

# Use the API
users = await api.user.get_users()

# Don't forget to close
await api.close()
```

### Error Handling

```python
from marzbanapilib import MarzbanAPI

async with MarzbanAPI(...) as api:
    try:
        user = await api.user.get_user("nonexistent")
    except ValueError as e:
        print(f"User not found: {e}")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
```

### Filtering Users

```python
# Get active users with pagination
users = await api.user.get_users(
    offset=0,
    limit=50,
    status="active",
    sort="created_at"
)
```

## API Reference

### User Management
- `create_user(data)` - Create new user
- `get_user(username)` - Get user details
- `modify_user(username, data)` - Modify user
- `delete_user(username)` - Delete user
- `get_users(**filters)` - List users with filters
- `reset_data_usage(username)` - Reset user data usage
- `revoke_subscription(username)` - Revoke user subscription
- `get_usage(username)` - Get user usage statistics
- And more...

### System Management
- `get_stats()` - Get system statistics
- `get_inbounds()` - Get inbound configurations
- `get_hosts()` - Get proxy hosts
- `modify_hosts(data)` - Modify proxy hosts

### Core Management
- `get_stats()` - Get core statistics
- `restart()` - Restart Xray core
- `get_config()` - Get core configuration
- `modify_config(data)` - Modify core configuration

### Node Management
- `get_all()` - List all nodes
- `create(data)` - Create new node
- `get(node_id)` - Get node details
- `modify(node_id, data)` - Modify node
- `delete(node_id)` - Delete node
- `reconnect(node_id)` - Reconnect node
- `get_usage()` - Get nodes usage statistics

## Requirements

- Python 3.7+
- httpx
- pydantic
- aiofiles

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/DeepPythonist/marzbanapilib/issues). 