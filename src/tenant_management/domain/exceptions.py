"""
Domain exceptions for tenant management
"""

from src.core.domain.exceptions import EntityNotFoundError, EntityValidationError


class PlanNotFoundError(EntityNotFoundError):
    """Exception raised when a Plan is not found in the repository."""


class InvalidPlanError(EntityNotFoundError):
    """Exception raised when a Plan is not valid."""


class TenantNotFoundError(EntityNotFoundError):
    """Exception raised when a Tenant is not found in the repository."""


class InvalidTenantError(EntityValidationError):
    """Exception raised when a Tenant is not valid."""
