class DomainError(Exception):
    """
    Domain exception base class.
    """


class EntityValidationError(DomainError):
    """
    Exception raised when an entity validation fails.
    """


class EntityNotFoundError(DomainError):
    """
    Exception raised when an entity is not found.
    """
