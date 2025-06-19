"""
Example usage of MarzbanAPILib

This example demonstrates basic operations with the Marzban API:
- Authentication
- Getting system statistics
- Creating a new user
- Listing users
- Modifying user settings
- Deleting a user
"""

import asyncio
from datetime import datetime, timedelta
from marzbanapilib import MarzbanAPI


async def main():
    # Configuration
    BASE_URL = "http://127.0.0.1:8000"  # Your Marzban panel URL
    USERNAME = "admin"                   # Your admin username
    PASSWORD = "password"                # Your admin password
    
    # Create API client using context manager
    async with MarzbanAPI(BASE_URL, USERNAME, PASSWORD) as api:
        print("✅ Successfully connected to Marzban API")
        print("-" * 50)
        
        # 1. Get system statistics
        print("\n📊 System Statistics:")
        stats = await api.system.get_stats()
        print(f"  • Marzban Version: {stats['version']}")
        print(f"  • Total Users: {stats['total_user']}")
        print(f"  • Active Users: {stats['users_active']}")
        print(f"  • CPU Usage: {stats['cpu_usage']}%")
        print(f"  • Memory Used: {stats['mem_used'] / (1024**3):.2f} GB")
        
        # 2. Create a new user
        print("\n👤 Creating a new user...")
        new_user_data = {
            "username": f"test_user_{int(datetime.now().timestamp())}",
            "proxies": {
                "vmess": {},  # Default VMess settings
                "vless": {}   # Default VLESS settings
            },
            "expire": int((datetime.now() + timedelta(days=30)).timestamp()),  # 30 days
            "data_limit": 10 * 1024**3,  # 10 GB
            "data_limit_reset_strategy": "monthly",
            "status": "active",
            "note": "Created via API example"
        }
        
        try:
            new_user = await api.user.create_user(new_user_data)
            print(f"  ✅ User created: {new_user['username']}")
            print(f"  • Subscription URL: {new_user['subscription_url']}")
            print(f"  • Status: {new_user['status']}")
            print(f"  • Data Limit: {new_user['data_limit'] / (1024**3)} GB")
        except ValueError as e:
            print(f"  ❌ Failed to create user: {e}")
            new_user = None
        
        # 3. List users with filters
        print("\n📋 Listing active users:")
        users_response = await api.user.get_users(
            limit=5,
            status="active",
            sort="-created_at"  # Sort by newest first
        )
        
        users = users_response['users']
        print(f"  Found {users_response['total']} total users, showing {len(users)}:")
        for user in users:
            print(f"  • {user['username']}")
            print(f"    - Status: {user['status']}")
            print(f"    - Created: {user['created_at']}")
            print(f"    - Used Traffic: {user['used_traffic'] / (1024**2):.2f} MB")
        
        # 4. Get user details and usage
        if new_user:
            print(f"\n📊 Getting usage for user: {new_user['username']}")
            usage = await api.user.get_usage(new_user['username'])
            print(f"  • Total usage across all nodes:")
            for node_usage in usage['usages']:
                print(f"    - {node_usage['node_name']}: {node_usage['used_traffic'] / (1024**2):.2f} MB")
        
        # 5. Modify user settings
        if new_user:
            print(f"\n✏️ Modifying user: {new_user['username']}")
            modified_data = {
                "data_limit": 20 * 1024**3,  # Increase to 20 GB
                "note": "Modified via API example"
            }
            
            modified_user = await api.user.modify_user(new_user['username'], modified_data)
            print(f"  ✅ User modified successfully")
            print(f"  • New data limit: {modified_user['data_limit'] / (1024**3)} GB")
        
        # 6. Get inbound configurations
        print("\n🔌 Available Inbounds:")
        inbounds = await api.system.get_inbounds()
        for protocol, inbound_list in inbounds.items():
            print(f"  • {protocol.upper()}:")
            for inbound in inbound_list:
                print(f"    - {inbound['tag']} (port: {inbound.get('port', 'N/A')})")
        
        # 7. Get admin information
        print("\n👮 Current Admin Info:")
        admin_info = await api.admin.get_current()
        print(f"  • Username: {admin_info['username']}")
        print(f"  • Is Sudo: {admin_info['is_sudo']}")
        print(f"  • Users Usage: {admin_info.get('users_usage', 0) / (1024**3):.2f} GB")
        
        # 8. Get nodes (if multi-node setup)
        print("\n🖥️ Nodes:")
        try:
            nodes = await api.node.get_all()
            if nodes:
                for node in nodes:
                    print(f"  • {node['name']} - {node['address']}:{node['port']}")
                    print(f"    - Status: {node['status']}")
                    print(f"    - Xray Version: {node.get('xray_version', 'N/A')}")
            else:
                print("  No additional nodes configured")
        except Exception:
            print("  Single node setup (no additional nodes)")
        
        # 9. Delete the test user
        if new_user:
            print(f"\n🗑️ Deleting test user: {new_user['username']}")
            try:
                await api.user.delete_user(new_user['username'])
                print("  ✅ User deleted successfully")
            except ValueError as e:
                print(f"  ❌ Failed to delete user: {e}")
        
        print("\n✅ Example completed successfully!")


async def manual_authentication_example():
    """Example of manual authentication without context manager"""
    print("\n📝 Manual Authentication Example:")
    
    # Create API instance
    api = MarzbanAPI("http://127.0.0.1:8000", "admin", "password")
    
    try:
        # Manually authenticate
        await api.authenticate()
        print("  ✅ Authenticated successfully")
        
        # Use the API
        stats = await api.system.get_stats()
        print(f"  • Total users: {stats['total_user']}")
        
    finally:
        # Always close the client
        await api.close()
        print("  ✅ Connection closed")


async def error_handling_example():
    """Example of error handling"""
    print("\n⚠️ Error Handling Example:")
    
    async with MarzbanAPI("http://127.0.0.1:8000", "admin", "password") as api:
        # Try to get a non-existent user
        try:
            user = await api.user.get_user("non_existent_user")
        except ValueError as e:
            print(f"  • Expected error: {e}")
        
        # Try to create a user with invalid data
        try:
            invalid_user = await api.user.create_user({
                "username": "a",  # Too short
                "proxies": {}     # No proxies defined
            })
        except ValueError as e:
            print(f"  • Validation error: {e}")


if __name__ == "__main__":
    # Run the main example
    asyncio.run(main())
    
    # Run additional examples
    asyncio.run(manual_authentication_example())
    asyncio.run(error_handling_example()) 