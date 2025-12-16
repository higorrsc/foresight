from typing import List, Set

from fastapi import Depends, HTTPException, status

from src.identity_access_management.domain.entities import User

from .auth import get_current_user


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


class PermissionChecker:
    """
    Dependency that checks if the current user has the required permission.
    """

    def __init__(self, required_permissions: List[str]):
        """
        Initialize the PermissionChecker with a list of required permissions.
        """

        self._required_permissions = set(required_permissions)

    def __call__(self, current_user: User = Depends(get_current_user)):
        """
        Check if the current user has any of the required permissions.
        """

        user_permissions: Set[str] = (
            current_user.permissions if current_user.permissions else set()
        )
        common_permissions = self._required_permissions.intersection(user_permissions)

        if not common_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Operation not permitted. Required permissions: "
                    f"{', '.join(self._required_permissions)}"
                ),
            )
