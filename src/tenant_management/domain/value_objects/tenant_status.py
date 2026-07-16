from enum import StrEnum


class TenantStatus(StrEnum):
    """
    Value Object that represents the status of a tenant.
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    TRIAL = "trial"

    @classmethod
    def get_all_status(cls):
        """
        Get all status
        """

        return [tenant_status.value for tenant_status in cls]
