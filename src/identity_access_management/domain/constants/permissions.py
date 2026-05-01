from enum import Enum


class AppPermission(str, Enum):
    """
    Application permissions
    """

    AREA_CREATE = "area:create"
    AREA_DELETE = "area:delete"
    AREA_READ = "area:read"
    AREA_UPDATE = "area:update"

    ORGANIZATIONAL_UNIT_CREATE = "organizational_unit:create"
    ORGANIZATIONAL_UNIT_DELETE = "organizational_unit:delete"
    ORGANIZATIONAL_UNIT_READ = "organizational_unit:read"
    ORGANIZATIONAL_UNIT_UPDATE = "organizational_unit:update"

    FINANCIAL_SCENARIO_CREATE = "financial_scenario:create"
    FINANCIAL_SCENARIO_DELETE = "financial_scenario:delete"
    FINANCIAL_SCENARIO_READ = "financial_scenario:read"
    FINANCIAL_SCENARIO_UPDATE = "financial_scenario:update"

    PLAN_CREATE = "plan:create"
    PLAN_DELETE = "plan:delete"
    PLAN_READ = "plan:read"
    PLAN_UPDATE = "plan:update"

    ROLE_CREATE = "role:create"
    ROLE_DELETE = "role:delete"
    ROLE_READ = "role:read"
    ROLE_SET_PERMISSIONS = "role:set_permissions"
    ROLE_UPDATE = "role:update"

    TENANT_READ = "tenant:read"
    TENANT_UPDATE = "tenant:update"

    USER_CHANGE_PASSWORD = "user:change_password"
    USER_CREATE = "user:create"
    USER_DELETE = "user:delete"
    USER_ME = "user:me"
    USER_READ = "user:read"
    USER_SET_PERMISSIONS = "user:set_permissions"
    USER_SET_ROLES = "user:set_roles"
    USER_UPDATE = "user:update"
    USER_UPDATE_PROFILE = "user:update_profile"

    @classmethod
    def get_all_permissions(cls) -> set[str]:
        """
        Get all permissions
        """

        return {permission.value for permission in cls}

    @classmethod
    def get_guest_permissions(cls) -> set[str]:
        """
        Returns the set of guest permissions.
        """

        return {
            cls.USER_ME.value,
            cls.USER_UPDATE_PROFILE.value,
            cls.USER_CHANGE_PASSWORD.value,
            cls.PLAN_READ,
        }

    @classmethod
    def get_admin_permissions(cls) -> set[str]:
        """
        Returns the set of admin permissions.
        """

        return cls.get_all_permissions()
