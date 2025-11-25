from .auth_router import router as AuthRouter
from .permission_router import router as PermissionRouter
from .role_router import router as RoleRouter
from .user_router import router as UserRouter

__all__ = [
    "AuthRouter",
    "PermissionRouter",
    "RoleRouter",
    "UserRouter",
]
