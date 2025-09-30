from typing import List

from fastapi import Depends, HTTPException, status

from src.api.dependencies.auth import get_current_user
from src.core.domain.entities.user import User


class RoleChecker:
    """
    Dependency that checks if the current user has the required role.
    """

    def __init__(self, allowed_roles: List[str]):
        """
        Initialize the RoleChecker with a list of allowed roles.
        """

        self._allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        """
        Check if the current user has any of the allowed roles.
        """

        if not any(current_user.has_role(role) for role in self._allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted: Insufficient permissions",
            )
