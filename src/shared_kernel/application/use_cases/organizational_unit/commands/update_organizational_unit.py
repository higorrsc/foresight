from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from src.shared_kernel.application.use_cases.organizational_unit import (
    InvalidOrganizationalUnitError,
)
from src.shared_kernel.domain._shared.exceptions import (
    EntityNotFoundException,
    EntityValidationError,
)
from src.shared_kernel.domain.repositories import IOrganizationalUnitRepository


@dataclass(frozen=True)
class CreateOrganizationalUnitInputDTO:
    """
    Data Transfer Object for input data when creating a new Organizational Unit.
    """

    id: UUID
    description: str
    code: str
    parent_id: Optional[UUID] = field(default=None)


@dataclass(frozen=True)
class CreateOrganizationalUnitOutputDTO:
    """
    Data Transfer Object for output data when creating a new Organizational Unit.
    """


class UpdateOrganizationalUnitUseCase:
    """
    Use case for updating an existing organizational unit.
    """

    def __init__(self, repository: IOrganizationalUnitRepository) -> None:
        """
        Initialize the UpdateOrganizationalUnitUseCase.
        """

        self._repository = repository

    def execute(self, input_dto: CreateOrganizationalUnitInputDTO) -> None:
        """
        Execute the use case to update an existing Organizational Unit.
        """

        entity = self._repository.get_by_id(input_dto.id)
        if not entity:
            raise EntityNotFoundException("Organizational Unit with given ID not found")

        try:
            entity.description = input_dto.description
            entity.code = input_dto.code
            entity.parent_id = input_dto.parent_id
        except EntityValidationError as e:
            raise InvalidOrganizationalUnitError(f"Invalid input data: {e}") from e

        self._repository.update(entity)
