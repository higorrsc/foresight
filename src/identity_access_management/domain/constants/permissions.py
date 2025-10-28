from enum import Enum


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
    USER_ME = "user:me"

    AREA_CREATE = "area:create"
    AREA_READ = "area:read"
    AREA_UPDATE = "area:update"
    AREA_DELETE = "area:delete"

    @classmethod
    def get_all_permissions(cls):
        """
        Get all permissions
        """

        return [permission.value for permission in cls]
