from dataclasses import dataclass
from typing import Generic, List, TypeVar

from src.core.domain._shared.repository import AbstractRepository

T = TypeVar("T")


@dataclass(frozen=True)
class ListRequestOutputDTO(Generic[T]):
    """
    Data Transfer Object for list requests.
    """

    data: List[T]


class GenericListUseCase(Generic[T]):
    """
    Use case for listing entities of type T.
    """

    def __init__(self, repository: AbstractRepository[T]) -> None:
        """
        Initialize the list use case.

        :param repository: The repository to use for listing entities.
        """

        self._repository = repository

    def execute(self) -> ListRequestOutputDTO:
        """
        Execute the list use case.

        :return: A list of entities.
        """

        entities = self._repository.list()
        return ListRequestOutputDTO(data=entities)
