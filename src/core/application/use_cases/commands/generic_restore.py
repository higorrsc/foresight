from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from src.core.domain import AbstractRepository
from src.core.domain.mixins import SoftDeletableMixin
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.exceptions import InsufficientPermissionError

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class RestoreRequestInputDTO:
    """
    Data Transfer Object for restore requests.
    """

    actor: "User"
    id: UUID


class GenericRestoreUseCase[T]:
    """
    Use case for deleting an entity of type T.
    """

    def __init__(
        self,
        repository: AbstractRepository[T],
        required_permission: AppPermission,
        not_found_exception: type[Exception],
        not_found_message: str = "Entity with id={id} not found",
    ) -> None:
        """
        Initialize the restore use case.

        :param repository: The repository to use for deleting entities.
        :param not_found_exception: The exception to raise when the entity is not found.
        :param not_found_message: The message to display when the entity is not found.
        """

        self._repository = repository
        self._required_permission = required_permission
        self._not_found_exception = not_found_exception
        self._not_found_message = not_found_message

    async def execute(self, request: RestoreRequestInputDTO) -> None:
        """
        Execute the restore use case.

        :param request: The restore request DTO containing the ID
                        of the entity to restore.
        """

        if self._required_permission not in request.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to restore data."
            )

        entity = self._repository.get_by_id(
            request.id,
            request.actor.tenant_id,
        )
        if entity is None:
            raise self._not_found_exception(
                self._not_found_message.format(id=request.id)
            )

        if isinstance(entity, SoftDeletableMixin):
            entity.restore()
            if hasattr(entity, "updated_by"):
                entity.updated_by = request.actor.id  # type: ignore
            await self._repository.update(entity)  # type: ignore
