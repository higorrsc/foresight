from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from src.core.domain import AbstractRepository, EntityValidationError
from src.core.domain.entities import DescribedEntity

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


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


class UpdateDescribedEntityUseCase[T: DescribedEntity]:
    """
    Update a existent entity.
    """

    def __init__(
        self,
        repository: AbstractRepository[T],
        not_found_exception: type[Exception],
        invalid_data_exception: type[Exception],
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
            if hasattr(entity, "updated_by"):
                entity.updated_by = input_dto.actor.id  # type: ignore
            entity.validate()
        except EntityValidationError as e:
            raise self._invalid_data_exception(f"Invalid input data: {e}") from e

        self._repository.update(entity)
        return UpdateDescribedEntityOutputDTO(
            id=entity.id,
            description=entity.description,
        )
