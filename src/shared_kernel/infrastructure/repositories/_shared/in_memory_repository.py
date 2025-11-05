import operator
from typing import Any, Dict, Generic, List, Optional, TypeVar
from uuid import UUID

from src.shared_kernel.domain._shared import AbstractRepository, PaginatedResult

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

    def get_by_id(
        self,
        entity_id: UUID,
        tenant_id: Optional[UUID],
    ) -> Optional[T]:
        """
        Retrieve an entity by its ID.

        :param entity_id: The ID of the entity to retrieve.
        :return: The entity if found, otherwise None.
        """

        for entity in self._entities:
            if entity.id == entity_id and getattr(entity, "tenant_id", None) == tenant_id:  # type: ignore
                return entity

        return None

    def list(
        self,
        tenant_id: Optional[UUID],
    ) -> List[T]:
        """
        List all entities in the repository.

        :return: A list of all entities.
        """
        if tenant_id:
            return [
                entity
                for entity in self._entities
                if getattr(entity, "tenant_id", None) == tenant_id
            ]

        return list(self._entities)

    def update(self, entity: T) -> Optional[T]:
        """
        Update an existing entity in the repository.

        :param entity: The entity to be updated.
        :return: None
        """

        tenant_id = getattr(entity, "tenant_id", None)
        old_entity = self.get_by_id(
            entity.id,  # type: ignore
            tenant_id,
        )

        if old_entity:
            self._entities.remove(old_entity)
            self._entities.append(entity)
            return entity

        return None

    def delete(self, entity_id: UUID, tenant_id: Optional[UUID]) -> None:
        """
        Delete an entity from the repository.

        :param entity_id: The ID of the entity to be deleted.
        """

        entity = self.get_by_id(
            entity_id,
            tenant_id,
        )

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
        tenant_id: Optional[UUID],
        filters: Optional[Dict[str, Any]] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
        offset: int = 0,
        limit: int = 100,
        include_inactive: bool = False,
    ) -> PaginatedResult[T]:
        """
        Search entities in the repository based on filters, sorting, and pagination.
        """

        results = [
            e for e in self._entities if getattr(e, "tenant_id", None) == tenant_id
        ]

        if not include_inactive:
            results = [
                e for e in results if hasattr(e, "is_active") and e.is_active  # type: ignore
            ]

        filtered_results = self.__apply_filters(results, filters or {})
        total = len(filtered_results)
        sorted_results = self.__apply_sorting(filtered_results, sort_by, sort_order)
        paginated_data = sorted_results[offset : offset + limit]

        return PaginatedResult(
            data=paginated_data,
            total=total,
        )
