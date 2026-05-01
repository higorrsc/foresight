class FinancialScenarioNotFoundError(Exception):
    """
    Exception raised when a Financial Scenario is not found in the repository.
    """


class InvalidFinancialScenarioError(Exception):
    """
    Exception raised when a Financial Scenario is not valid.
    """


class CannotUpdateLockedFinancialScenarioError(Exception):
    """
    Exception raised when a Financial Scenario is locked and cannot be updated.
    """


class FinancialScenarioAlreadyLockedError(Exception):
    """
    Exception raised when a Financial Scenario is already locked.
    """


class FinancialScenarioAlreadyUnlockedError(Exception):
    """
    Exception raised when a Financial Scenario is already unlocked.
    """
