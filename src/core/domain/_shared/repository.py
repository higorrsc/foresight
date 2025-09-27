from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, Optional, TypeVar
from uuid import UUID

T = TypeVar("T")


@dataclass
class PaginatedResult(Generic[T]):
    """
    Paginated result of list operations.
    """

    data: List[T]
    total: int


class AbstractRepository(ABC, Generic[T]):
    """
    Abstract base class for a repository that handles entities of type T.
    """

    @abstractmethod
    def save(self, entity: T) -> Optional[T]:
        """
        Save an entity to the repository.

        :param entity: The entity to be saved.
        """

        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, entity_id: UUID) -> Optional[T]:
        """
        Retrieve an entity by its ID.

        :param entity_id: The ID of the entity to retrieve.
        :return: The entity if found, otherwise None.
        """

        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[T]:
        """
        List all entities in the repository.

        :return: A list of all entities.
        """

        raise NotImplementedError

    @abstractmethod
    def update(self, entity: T) -> Optional[T]:
        """
        Update an existing entity in the repository.

        :param entity: The entity to be updated.
        :return: The updated entity.
        """

        raise NotImplementedError

    @abstractmethod
    def delete(self, entity_id: UUID) -> None:
        """
        Delete an entity from the repository.

        :param entity_id: The ID of the entity to be deleted.
        """

        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
        offset: int = 0,
        limit: int = 10,
    ) -> PaginatedResult[T]:
        """
        Search for entities based on criteria, with sorting and pagination.
        """

        raise NotImplementedError
