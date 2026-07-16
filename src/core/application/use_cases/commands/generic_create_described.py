from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from src.core.domain import AbstractRepository, EntityValidationError
from src.core.domain.entities import DescribedEntity
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.exceptions import InsufficientPermissionError

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class CreateDescribedEntityInputDTO:
    """
    Data Transfer Object for input data when creating a new entity.
    """

    actor: "User"
    description: str
    id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True)
class CreateDescribedEntityOutputDTO:
    """
    Data Transfer Object for output data when creating a new entity.
    """

    id: UUID


class CreateDescribedEntityUseCase[T: DescribedEntity]:
    """
    Create a new entity.
    """

    def __init__(
        self,
        repository: AbstractRepository[T],
        required_permission: AppPermission,
        entity_cls: type[T],
        invalid_data_exception: type[Exception],
    ) -> None:
        """
        Initialize the CreateDescribedEntityUseCase.
        """

        self._repository = repository
        self._required_permission = required_permission
        self._entity_cls = entity_cls
        self._invalid_data_exception = invalid_data_exception

    async def execute(
        self,
        input_dto: CreateDescribedEntityInputDTO,
    ) -> CreateDescribedEntityOutputDTO:
        """
        Execute the use case to create a new entity.
        """

        if self._required_permission not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to list data."
            )

        try:
            entity = self._entity_cls(
                id=input_dto.id,
                tenant_id=input_dto.actor.tenant_id,
                description=input_dto.description,
            )
        except EntityValidationError as e:
            raise self._invalid_data_exception(f"Invalid input data: {e}") from e

        await self._repository.save(entity)
        return CreateDescribedEntityOutputDTO(id=entity.id)
