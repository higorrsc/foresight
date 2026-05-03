"""
Domain exceptions for Shared Kernel bounded context.
"""

from src.core.domain.exceptions import (
    EntityNotFoundError,
    EntityValidationError,
)


class AreaNotFoundError(EntityNotFoundError):
    """Exception raised when an Area is not found in the repository."""


class InvalidAreaError(EntityValidationError):
    """Exception raised when an Area is not valid."""


class InvalidOrganizationalUnitError(EntityValidationError):
    """Exception raised when an Organizational Unit is not valid."""


class OrganizationalUnitNotFoundError(EntityNotFoundError):
    """Exception raised when an Organizational Unit is not found in the repository."""
