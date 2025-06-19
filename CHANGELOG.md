# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-12-19

### Added
- **Token Authentication Support**: You can now authenticate directly using a pre-existing JWT access token
  - New optional parameter `access_token` in `MarzbanAPI` constructor
  - Choose between username/password authentication or direct token authentication
  - Backward compatible with existing code

### Changed
- `username` and `password` parameters are now optional in `MarzbanAPI` constructor (when `access_token` is provided)
- Updated documentation and examples to show both authentication methods

### Examples
```python
# New: Direct token authentication
async with MarzbanAPI("http://127.0.0.1:8000", access_token="your_jwt_token") as api:
    users = await api.user.get_users()

# Still works: Username/password authentication  
async with MarzbanAPI("http://127.0.0.1:8000", "admin", "password") as api:
    users = await api.user.get_users()
```

## [0.1.0] - 2024-12-18

### Added
- Initial release of MarzbanAPILib
- Modular API client with separate sections for User, Admin, System, Core, and Node management
- Full async/await support with modern Python patterns
- Complete type hints and comprehensive error handling
- Support for all Marzban API endpoints (35+ methods)
- Context manager support for automatic connection management
- Detailed documentation and usage examples 