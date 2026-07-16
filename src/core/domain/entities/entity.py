from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from src.core.domain import Notification


@dataclass(kw_only=True, eq=False, repr=False)
class AbstractEntity(ABC):
    """
    Abstract base class for entities in the domain layer.
    """

    id: UUID = field(default_factory=uuid4)
    notification: Notification = field(default_factory=Notification, init=False)

    def _repr_fields(self) -> str:
        """
        Returns a string representation of the entity's fields.

        Returns:
            str: A string representation of the entity's fields.
        """

        return f"id={self.id}"

    def _str_fields(self) -> str:
        """
        Returns a string representation of the entity's fields.

        Returns:
            str: A string representation of the entity's fields.
        """

        return f"id={self.id}"

    def __eq__(self, other) -> bool:
        """
        Check if two entities are equal.

        Two entities are considered equal if they have the same ID.

        Args:
            other (object): The object to compare with.

        Returns:
            bool: True if the two entities are equal, False otherwise.
        """

        if not isinstance(other, AbstractEntity):
            return False

        return self.id == other.id

    def __post_init__(self) -> None:
        """
        Validate the entity after initialization.
        """

        self.validate()

    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the OrganizationalUnit entity.
        """

        return f"<{self.__class__.__name__} {self._repr_fields()}>"

    def __str__(self) -> str:
        """
        Returns a string representation of the OrganizationalUnit entity.
        """

        return f"{self.__class__.__name__} ({self._str_fields()})"

    @abstractmethod
    def validate(self) -> None:
        """
        Validate the entity.

        This method should be implemented in the concrete subclasses to validate
        the entity's state. It should raise a ValueError if the entity is in an
        invalid state.

        Raises:
            ValueError: If the entity is in an invalid state.
        """

        raise NotImplementedError  # pragma: no cover
