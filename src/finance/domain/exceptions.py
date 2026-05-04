"""
Domain exception for finance bounded context
"""

from src.core.domain.exceptions import EntityValidationError


class CurrencyMismatchError(EntityValidationError):
    """Raised when an operation is attempted between different currencies."""


class InvalidMoneyOperationError(EntityValidationError):
    """Raised when an invalid operation is attempted on a Money object."""
