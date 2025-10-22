from dataclasses import dataclass
from typing import Generic, Type, TypeVar
from uuid import UUID

from src.core.domain._shared import AbstractRepository, SoftDeletableMixin

T = TypeVar("T")


@dataclass(frozen=True)
class RestoreRequestInputDTO:
    """
    Data Transfer Object for restore requests.
    """

    id: UUID


class GenericRestoreUseCase(Generic[T]):
    """
    Use case for deleting an entity of type T.
    """

    def __init__(
        self,
        repository: AbstractRepository[T],
        not_found_exception: Type[Exception],
        not_found_message: str = "Entity with id={id} not found",
    ) -> None:
        """
        Initialize the restore use case.

        :param repository: The repository to use for deleting entities.
        :param not_found_exception: The exception to raise when the entity is not found.
        :param not_found_message: The message to display when the entity is not found.
        """

        self._repository = repository
        self._not_found_exception = not_found_exception
        self._not_found_message = not_found_message

    def execute(self, request: RestoreRequestInputDTO) -> None:
        """
        Execute the restore use case.

        :param request: The restore request DTO containing the ID of the entity to restore.
        """

        entity = self._repository.get_by_id(request.id)
        if entity is None:
            raise self._not_found_exception(
                self._not_found_message.format(id=request.id)
            )

        if isinstance(entity, SoftDeletableMixin):
            entity.restore()
            self._repository.update(entity)
