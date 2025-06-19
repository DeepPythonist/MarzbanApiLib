"""
MarzbanAPILib - A Python client library for Marzban VPN panel API

This library provides a modular and easy-to-use interface for interacting
with the Marzban VPN panel through its REST API.
"""

__version__ = "0.2.0"
__author__ = "Mohammad Rasol Esfandiari"
__email__ = "mrasolesfandiari@gmail.com"
__license__ = "MIT"

# Main API class
from .marzban import MarzbanAPI

# Section classes (optional direct imports)
from .sections.user import UserAPI
from .sections.admin import AdminAPI
from .sections.system import SystemAPI
from .sections.core import CoreAPI
from .sections.node import NodeAPI

# Utility functions
from .utils import get_token_from_credentials

__all__ = [
    "MarzbanAPI",
    "UserAPI",
    "AdminAPI", 
    "SystemAPI",
    "CoreAPI",
    "NodeAPI",
    "get_token_from_credentials",
] 