class PermissionAlreadyExistsError(Exception):
    """
    Exception raised when a Permission already exists in the repository.
    """


class PermissionNotFoundError(Exception):
    """
    Exception raised when a PermissionAlreadyExistsError(Exception):
    """


class InsufficientPermissionError(Exception):
    """
    Exception raised when the actor does not have sufficient
    permissions to perform an action.
    """
