import operator
from typing import Any, Generic, TypeVar
from uuid import UUID

from src.core.domain import AbstractRepository, PaginatedResult
from src.core.domain.entities import AbstractEntity

T = TypeVar("T", bound=AbstractEntity)


class InMemoryRepository(AbstractRepository[T], Generic[T]):
    """
    A simple in-memory implementation of AbstractRepository for testing.
    """

    def __init__(self, entities: list[T] | None = None):
        """
        Initialize the repository with an optional list of entities.
        """

        self._entities = entities or []

    def save(self, entity: T) -> T | None:
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
        tenant_id: UUID | None,
    ) -> T | None:
        """
        Retrieve an entity by its ID.

        :param entity_id: The ID of the entity to retrieve.
        :return: The entity if found, otherwise None.
        """

        for entity in self._entities:
            if (
                entity.id == entity_id
                and getattr(entity, "tenant_id", None) == tenant_id
            ):  # type: ignore
                return entity

        return None

    def get_all(
        self,
        tenant_id: UUID | None,
    ) -> list[T]:
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

    def update(self, entity: T) -> T | None:
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

    def delete(self, entity_id: UUID, tenant_id: UUID | None) -> None:
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

    def __entity_matches_filters(self, entity: T, filters: dict[str, Any]) -> bool:
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

    def __apply_filters(self, entities: list[T], filters: dict[str, Any]) -> list[T]:
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
        self, entities: list[T], sort_by: str | None, sort_order: str
    ) -> list[T]:
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
        tenant_id: UUID | None,
        filters: dict[str, Any] | None = None,
        sort_by: str | None = None,
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

        # Only filter by is_active if requested and if the entity has this attribute
        if not include_inactive and results and hasattr(results[0], "is_active"):
            results = [e for e in results if getattr(e, "is_active")]

        filtered_results = self.__apply_filters(results, filters or {})
        total = len(filtered_results)
        sorted_results = self.__apply_sorting(filtered_results, sort_by, sort_order)
        paginated_data = sorted_results[offset : offset + limit]

        return PaginatedResult(
            data=paginated_data,
            total=total,
        )
