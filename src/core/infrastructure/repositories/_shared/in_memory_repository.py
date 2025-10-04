import operator
from typing import Any, Dict, Generic, List, Optional, TypeVar
from uuid import UUID

from src.core.domain._shared import AbstractRepository, PaginatedResult

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

    def get_by_id(self, entity_id: UUID) -> Optional[T]:
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

    def __entity_matches_filters(self, entity: T, filters: Dict[str, Any]) -> bool:
        """
        Verify if an entity matches the given filters.
        """

        for field, value in filters.items():
            if not hasattr(entity, field):
                return False

            entity_value = getattr(entity, field)
            if value.lower() not in str(entity_value).lower():
                return False
        return True

    def __apply_filters(self, entities: List[T], filters: Dict[str, Any]) -> List[T]:
        """
        Apply filters to a list of entities.
        """

        if not filters:
            return entities

        return [
            entity
            for entity in entities
            if self.__entity_matches_filters(entity, filters)
        ]

    def __apply_sorting(
        self, entities: List[T], sort_by: Optional[str], sort_order: str
    ) -> List[T]:
        """
        Apply sorting to a list of entities.
        """

        if sort_by and (entities and hasattr(entities[0], sort_by)):
            entities.sort(
                key=operator.attrgetter(sort_by),
                reverse=sort_order.lower() == "desc",
            )
        return entities

    def search(
        self,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
        offset: int = 0,
        limit: int = 100,
    ) -> PaginatedResult[T]:
        """
        Search entities in the repository based on filters, sorting, and pagination.
        """
        filtered_results = self.__apply_filters(list(self._entities), filters or {})
        total = len(filtered_results)
        sorted_results = self.__apply_sorting(filtered_results, sort_by, sort_order)
        paginated_data = sorted_results[offset : offset + limit]

        return PaginatedResult(
            data=paginated_data,
            total=total,
        )
