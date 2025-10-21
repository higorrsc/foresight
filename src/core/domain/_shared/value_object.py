from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(kw_only=True)
class AbstractValueObject(ABC):
    """
    Abstract base class for value objects.
    """

    def __post_init__(self):
        """
        Validate the value object after initialization.
        """

        self._validate()

    @abstractmethod
    def _validate(self):
        """
        Validate the value object.

        This method should be implemented in the concrete subclasses to validate
        the value object's state. It should raise a ValueError if the value object is in an
        invalid state.

        Raises:
            ValueError: If the value object is in an invalid state.
        """

        raise NotImplementedError  # pragma: no cover
