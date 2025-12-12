class InvalidUserError(Exception):
    """
    Exception raised when a User is not valid.
    """


class UserUseCaseError(Exception):
    """
    Base class for user use case errors.
    """


class InvalidPasswordError(UserUseCaseError):
    """
    Exception raised when a password is invalid.
    """


class UserNotFoundError(UserUseCaseError):
    """
    Exception raised when a User is not found.
    """


class UsernameAlreadyExistsError(UserUseCaseError):
    """
    Raises when a username already exists.
    """
