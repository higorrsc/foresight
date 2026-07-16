"""
Domain exceptions for planning bounded context.
"""

from src.core.domain.exceptions import (
    BusinessRuleViolationError,
    EntityNotFoundError,
    EntityValidationError,
)


class CannotUpdateLockedScenarioError(BusinessRuleViolationError):
    """Exception raised when a Scenario is locked and cannot be updated."""


class InvalidScenarioError(EntityValidationError):
    """Exception raised when a Scenario is not valid."""


class ScenarioAlreadyLockedError(BusinessRuleViolationError):
    """Exception raised when a Scenario is already locked."""


class ScenarioAlreadyUnlockedError(BusinessRuleViolationError):
    """Exception raised when a Scenario is already unlocked."""


class ScenarioNotFoundError(EntityNotFoundError):
    """Exception raised when a Scenario is not found in the repository."""


class ExchangeRateNotFoundError(EntityNotFoundError):
    """Exception raised when an ExchangeRate is not found in the repository."""


class InvalidExchangeRateError(EntityValidationError):
    """Exception raised when an ExchangeRate is not valid."""
