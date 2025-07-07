# backend/core/__init__.py

# This file makes the 'core' directory a Python package.
# It can be used to make core components easily importable.

from .config import settings
from .database import get_async_db, async_engine, AsyncSessionLocal
from .security import oauth2_scheme, create_access_token, decode_access_token, get_password_hash, verify_password

__all__ = [
    "settings",
    "get_async_db",
    "async_engine",
    "AsyncSessionLocal",
    "oauth2_scheme",
    "create_access_token",
    "decode_access_token",
    "get_password_hash",
    "verify_password",
]
