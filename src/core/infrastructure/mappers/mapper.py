from abc import ABC, abstractmethod


class AbstractMapper[T, M](ABC):
    """
    Base contract for mappers between Entity <-> Model.
    """

    @abstractmethod
    def to_model(self, entity: T) -> M:
        """Converts an entity to a model."""

    @abstractmethod
    def to_entity(self, model: M) -> T:
        """Converts a model to an entity."""
