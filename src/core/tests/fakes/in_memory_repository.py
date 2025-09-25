from typing import Any, Generic, List, Optional, TypeVar
from uuid import UUID

from core.domain._shared import AbstractRepository

T = TypeVar("T")


class InMemoryRepository(AbstractRepository[T], Generic[T]):
    """
    A simple in-memory implementation of AbstractRepository for testing.
    """

    def __init__(self, entities: Optional[List[T]] = None):
        """
        Initialize the repository with an optional list of entities.
        """

        self._entities = entities or []

    def save(self, entity: T) -> Optional[T]:
        """
        Save an entity to the repository.

        :param entity: The entity to be saved.
        :return: None
        """

        self._entities.append(entity)
        return entity

    def get_by_id(self, entity_id: Any) -> Optional[T]:
        """
        Retrieve an entity by its ID.

        :param entity_id: The ID of the entity to retrieve.
        :return: The entity if found, otherwise None.
        """

        for entity in self._entities:
            if entity.id == entity_id:  # type: ignore
                return entity

        return None

    def list(self) -> List[T]:
        """
        List all entities in the repository.

        :return: A list of all entities.
        """

        return list(self._entities)

    def update(self, entity: T) -> Optional[T]:
        """
        Update an existing entity in the repository.

        :param entity: The entity to be updated.
        :return: None
        """

        old_entity = self.get_by_id(entity.id)  # type: ignore

        if old_entity:
            self._entities.remove(old_entity)
            self._entities.append(entity)
            return entity

        return None

    def delete(self, entity_id: UUID) -> None:
        """
        Delete an entity from the repository.

        :param entity_id: The ID of the entity to be deleted.
        """

        entity = self.get_by_id(entity_id)

        if entity:
            self._entities.remove(entity)
