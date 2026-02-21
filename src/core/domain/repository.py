from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar
from uuid import UUID

T = TypeVar("T")


@dataclass
class PaginatedResult(Generic[T]):
    """
    Paginated result of list operations.
    """

    data: list[T]
    total: int


class AbstractRepository(ABC, Generic[T]):
    """
    Abstract base class for a repository that handles entities of type T.
    """

    @abstractmethod
    def save(self, entity: T) -> T | None:
        """
        Save an entity to the repository.

        :param entity: The entity to be saved.
        """

        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_by_id(
        self,
        entity_id: UUID,
        tenant_id: UUID | None,
    ) -> T | None:
        """
        Retrieve an entity by its ID.

        :param entity_id: The ID of the entity to retrieve.
        :param tenant_id: The ID of the tenant.
        :return: The entity if found, otherwise None.
        """

        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_all(
        self,
        tenant_id: UUID | None,
    ) -> list[T]:
        """
        List all entities in the repository.

        :param tenant_id: The ID of the tenant.
        :return: A list of all entities.
        """

        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def update(self, entity: T) -> T | None:
        """
        Update an existing entity in the repository.

        :param entity: The entity to be updated.
        :return: The updated entity.
        """

        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def delete(
        self,
        entity_id: UUID,
        tenant_id: UUID | None,
    ) -> None:
        """
        Delete an entity from the repository.

        :param entity_id: The ID of the entity to be deleted.
        :param tenant_id: The ID of the tenant.
        """

        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def search(
        self,
        tenant_id: UUID | None,
        filters: dict[str, Any] | None = None,
        sort_by: str | None = None,
        sort_order: str = "asc",
        offset: int = 0,
        limit: int = 10,
        include_inactive: bool = False,
    ) -> PaginatedResult[T]:
        """
        Search for entities based on criteria, with sorting and pagination.
        """

        raise NotImplementedError  # pragma: no cover
