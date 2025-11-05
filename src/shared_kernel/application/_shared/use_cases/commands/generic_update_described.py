from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, Type, TypeVar
from uuid import UUID

from src.shared_kernel.domain._shared import AbstractRepository, EntityValidationError
from src.shared_kernel.domain._shared.entities import DescribedEntity

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User

T = TypeVar("T", bound=DescribedEntity)


@dataclass(frozen=True)
class UpdateDescribedEntityInputDTO:
    """
    Data Transfer Object for input data when updating a existent entity.
    """

    actor: "User"
    id: UUID
    description: str


@dataclass(frozen=True)
class UpdateDescribedEntityOutputDTO:
    """
    Data Transfer Object for output data when updating a existent entity.
    """

    id: UUID
    description: str


class UpdateDescribedEntityUseCase(Generic[T]):
    """
    Update a existent entity.
    """

    def __init__(
        self,
        repository: AbstractRepository[T],
        not_found_exception: Type[Exception],
        invalid_data_exception: Type[Exception],
    ) -> None:
        """
        Initialize the UpdateDescribedEntityUseCase.
        """

        self._repository = repository
        self._not_found_exception = not_found_exception
        self._invalid_data_exception = invalid_data_exception

    def execute(
        self,
        input_dto: UpdateDescribedEntityInputDTO,
    ) -> UpdateDescribedEntityOutputDTO:
        """
        Execute the use case to update a existent entity.
        """

        entity = self._repository.get_by_id(
            input_dto.id,
            input_dto.actor.tenant_id,
        )
        if not entity:
            raise self._not_found_exception(f"Entity with id {input_dto.id} not found")

        try:
            entity.update_description(input_dto.description)
        except EntityValidationError as e:
            raise self._invalid_data_exception(f"Invalid input data: {e}") from e

        self._repository.update(entity)
        return UpdateDescribedEntityOutputDTO(
            id=entity.id,
            description=entity.description,
        )
