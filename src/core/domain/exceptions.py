class DomainException(Exception):
    """
    Domain exception base class.
    """


class EntityValidationError(DomainException):
    """
    Exception raised when an entity validation fails.
    """


class EntityNotFoundException(DomainException):
    """
    Exception raised when an entity is not found.
    """
