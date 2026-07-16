from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from src.core.domain import AbstractRepository
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.exceptions import InsufficientPermissionError

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class GetByIdRequestInputDTO:
    """
    Data Transfer Object for get by id requests.
    """

    actor: "User"
    id: UUID


class GenericGetByIdUseCase[T]:
    """
    Use case for getting an entity by its ID.
    """

    def __init__(
        self,
        repository: AbstractRepository[T],
        required_permission: AppPermission,
        not_found_exception: type[Exception],
        not_found_message: str = "Entity with id={id} not found",
    ):
        """
        Initialize the get by id use case.

        :param repository: The repository to use for getting entities.
        :param not_found_exception: The exception to raise when the entity is not found.
        :param not_found_message: The message to display when the entity is not found.
        """

        self._repository = repository
        self._required_permission = required_permission
        self._not_found_exception = not_found_exception
        self._not_found_message = not_found_message

    async def execute(self, request: GetByIdRequestInputDTO) -> T:
        """
        Execute the get by id use case.

        :param request: The get by id request DTO containing the ID
                        of the entity to get.
        :return: The entity with the given ID.
        """

        if self._required_permission not in request.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to read data."
            )

        entity = await self._repository.get_by_id(
            request.id,
            request.actor.tenant_id,
        )
        if entity is None:
            raise self._not_found_exception(
                self._not_found_message.format(id=request.id)
            )

        return entity
