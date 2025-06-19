"""
MarzbanAPILib CLI entry point

This module is executed when running: python -m marzbanapilib
"""

from . import __version__, __author__, __license__


def main():
    """Display package information"""
    print(f"""
MarzbanAPILib v{__version__}
{'=' * 40}
A modern async Python client library for Marzban VPN panel API

Author: {__author__}
License: {__license__}

Usage:
    import asyncio
    from marzbanapilib import MarzbanAPI
    
    async def example():
        async with MarzbanAPI("http://127.0.0.1:8000", "admin", "password") as api:
            stats = await api.system.get_stats()
            print(f"Total users: {{stats['total_user']}}")
    
    asyncio.run(example())

For more examples, see: examples/usage_example.py
Documentation: https://github.com/DeepPythonist/marzbanapilib
""")


if __name__ == "__main__":
    main() 