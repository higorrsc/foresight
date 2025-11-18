class TenantNotFoundError(Exception):
    """
    Exception raised when a Tenant is not found in the repository.
    """


class InvalidTenantError(Exception):
    """
    Exception raised when a Tenant is not valid.
    """
