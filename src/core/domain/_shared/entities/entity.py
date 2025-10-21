from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from src.core.domain._shared import Notification


@dataclass(kw_only=True, eq=False)
class AbstractEntity(ABC):
    """
    Abstract base class for entities in the domain layer.
    """

    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    notification: Notification = field(default_factory=Notification, init=False)

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

        self._validate()

    @abstractmethod
    def _validate(self) -> None:
        """
        Validate the entity.

        This method should be implemented in the concrete subclasses to validate
        the entity's state. It should raise a ValueError if the entity is in an
        invalid state.

        Raises:
            ValueError: If the entity is in an invalid state.
        """

        raise NotImplementedError  # pragma: no cover
