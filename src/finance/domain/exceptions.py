"""
Domain exception for finance bounded context
"""

from src.core.domain.exceptions import DomainError


class CurrencyDomainError(DomainError):
    """Base currency domain exception."""


class CurrencyMismatchError(CurrencyDomainError):
    """Raised when an operation is attempted between different currencies."""


class CurrencyNotFoundError(CurrencyDomainError):
    """Raised when a currency does not exist."""


class InvalidCurrencyCodeError(CurrencyDomainError):
    """Raised when a currency code is invalid."""


class InvalidMoneyOperationError(CurrencyDomainError):
    """Raised when an invalid operation is attempted on a Money object."""
