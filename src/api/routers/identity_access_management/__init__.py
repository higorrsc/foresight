from .auth_router import router as AuthRouter
from .role_router import router as RoleRouter
from .user_router import protected_router as UserProtectedRouter
from .user_router import public_router as UserPublicRouter

__all__ = [
    "AuthRouter",
    "RoleRouter",
    "UserProtectedRouter",
    "UserPublicRouter",
]
