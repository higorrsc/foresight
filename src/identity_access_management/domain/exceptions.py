"""
Domain exceptions for Identity Access Management bounded context.
"""

from src.core.domain.exceptions import (
    AuthorizationError,
    BusinessRuleViolationError,
    ConflictError,
    EntityNotFoundError,
    EntityValidationError,
)


class InsufficientPermissionError(AuthorizationError):
    """Exception raised when user has insufficient permissions."""


class InvalidPasswordError(EntityValidationError):
    """Exception raised when password is invalid."""


class InvalidRoleError(EntityValidationError):
    """Exception raised when role is invalid."""


class InvalidTokenError(AuthorizationError):
    """Exception raised when token is invalid."""


class InvalidUserError(EntityValidationError):
    """Exception raised when user is invalid."""


class PermissionAlreadyExistsError(ConflictError):
    """Exception raised when permission already exists."""


class PermissionNotFoundError(EntityNotFoundError):
    """Exception raised when permission is not found."""


class RoleAlreadyExistsError(ConflictError):
    """Exception raised when role already exists."""


class RoleDeletionIntegrityError(BusinessRuleViolationError):
    """Exception raised when role is in use and cannot be deleted."""


class RoleNotFoundError(EntityNotFoundError):
    """Exception raised when role is not found."""


class UsernameAlreadyExistsError(ConflictError):
    """Exception raised when username already exists."""


class UserNotFoundError(EntityNotFoundError):
    """Exception raised when user is not found."""
