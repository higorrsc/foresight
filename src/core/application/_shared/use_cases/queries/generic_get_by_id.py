from dataclasses import dataclass
from typing import Generic, Type, TypeVar
from uuid import UUID

from src.core.domain._shared import AbstractRepository

T = TypeVar("T")


@dataclass(frozen=True)
class GetByIdRequestInputDTO:
    """
    Data Transfer Object for get by id requests.
    """

    id: UUID


class GenericGetByIdUseCase(Generic[T]):
    """
    Use case for getting an entity by its ID.
    """

    def __init__(
        self,
        repository: AbstractRepository[T],
        not_found_exception: Type[Exception],
        not_found_message: str = "Entity with id={id} not found",
    ):
        """
        Initialize the get by id use case.

        :param repository: The repository to use for getting entities.
        :param not_found_exception: The exception to raise when the entity is not found.
        :param not_found_message: The message to display when the entity is not found.
        """

        self._repository = repository
        self._not_found_exception = not_found_exception
        self._not_found_message = not_found_message

    def execute(self, request: GetByIdRequestInputDTO) -> T:
        """
        Execute the get by id use case.

        :param request: The get by id request DTO containing the ID of the entity to get.
        :return: The entity with the given ID.
        """

        entity = self._repository.get_by_id(request.id)
        if entity is None:
            raise self._not_found_exception(
                self._not_found_message.format(id=request.id)
            )

        return entity
