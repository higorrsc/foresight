from enum import Enum
from typing import Set


class AppPermission(str, Enum):
    """
    Application permissions
    """

    ROLE_CREATE = "role:create"
    ROLE_READ = "role:read"
    ROLE_UPDATE = "role:update"
    ROLE_DELETE = "role:delete"

    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    USER_SET_ROLES = "user:set_roles"
    USER_SET_PERMISSIONS = "user:set_permissions"
    USER_UPDATE_PROFILE = "user:update_profile"
    USER_CHANGE_PASSWORD = "user:change_password"
    USER_ME = "user:me"

    AREA_CREATE = "area:create"
    AREA_READ = "area:read"
    AREA_UPDATE = "area:update"
    AREA_DELETE = "area:delete"

    @classmethod
    def get_all_permissions(cls) -> Set[str]:
        """
        Get all permissions
        """

        return {permission.value for permission in cls}

    @classmethod
    def get_guest_permissions(cls) -> Set[str]:
        """
        Returns the set of guest permissions.
        """

        return {
            cls.USER_ME.value,
            cls.USER_UPDATE_PROFILE.value,
            cls.USER_CHANGE_PASSWORD.value,
        }

    @classmethod
    def get_admin_permissions(cls) -> Set[str]:
        """
        Returns the set of admin permissions.
        """

        return cls.get_all_permissions()
