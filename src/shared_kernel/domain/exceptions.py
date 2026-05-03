"""
Domain exceptions for Shared Kernel bounded context.
"""

from src.core.domain.exceptions import (
    BusinessRuleViolationError,
    EntityNotFoundError,
    EntityValidationError,
)


class AreaNotFoundError(EntityNotFoundError):
    """Exception raised when an Area is not found in the repository."""


class CannotUpdateLockedFinancialScenarioError(BusinessRuleViolationError):
    """Exception raised when a Financial Scenario is locked and cannot be updated."""


class FinancialScenarioAlreadyLockedError(BusinessRuleViolationError):
    """Exception raised when a Financial Scenario is already locked."""


class FinancialScenarioAlreadyUnlockedError(BusinessRuleViolationError):
    """Exception raised when a Financial Scenario is already unlocked."""


class FinancialScenarioNotFoundError(EntityNotFoundError):
    """Exception raised when a Financial Scenario is not found in the repository."""


class InvalidAreaError(EntityValidationError):
    """Exception raised when an Area is not valid."""


class InvalidFinancialScenarioError(EntityValidationError):
    """Exception raised when a Financial Scenario is not valid."""


class InvalidOrganizationalUnitError(EntityValidationError):
    """Exception raised when an Organizational Unit is not valid."""


class OrganizationalUnitNotFoundError(EntityNotFoundError):
    """Exception raised when an Organizational Unit is not found in the repository."""
