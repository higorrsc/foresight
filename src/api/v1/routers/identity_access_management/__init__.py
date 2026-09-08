from .auth_router import router as auth_router
from .permission_router import router as permission_router
from .role_router import router as role_router
from .user_router import router as user_router

__all__ = [
    "auth_router",
    "permission_router",
    "role_router",
    "user_router",
]
