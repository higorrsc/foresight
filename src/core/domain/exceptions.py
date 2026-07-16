"""
Core domain exceptions.
"""


class DomainError(Exception):
    """Domain exception base class."""


class AuthorizationError(DomainError):
    """Raised when authorization fails."""


class BusinessRuleViolationError(DomainError):
    """Raised when a business rule is violated."""


class ConflictError(BusinessRuleViolationError):
    """Raised when resource uniqueness/integrity conflicts occur."""


class EntityNotFoundError(DomainError):
    """Exception raised when an entity is not found."""


class EntityValidationError(DomainError):
    """Exception raised when an entity validation fails."""
