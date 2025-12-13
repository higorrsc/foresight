class RoleNotFoundError(Exception):
    """
    Exception raised when a Role is not found in the repository.
    """


class InvalidRoleError(Exception):
    """
    Exception raised when a Role is not valid.
    """


class RoleAlreadyExistsError(Exception):
    """
    Exception raised when a Role already exists in the repository.
    """


class RoleDeletionIntegrityError(Exception):
    """
    Exception raised when a Role has association with any user.
    """
