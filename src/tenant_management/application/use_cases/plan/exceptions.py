class PlanNotFoundError(Exception):
    """
    Exception raised when a Plan is not found in the repository.
    """


class InvalidPlanError(Exception):
    """
    Exception raised when a Plan is not valid.
    """
