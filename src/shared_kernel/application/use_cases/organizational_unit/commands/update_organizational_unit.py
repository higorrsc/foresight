from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from src.core.domain.exceptions import EntityValidationError
from src.shared_kernel.application.use_cases.organizational_unit import (
    InvalidOrganizationalUnitError,
)
from src.shared_kernel.application.use_cases.organizational_unit.exceptions import (
    OrganizationalUnitNotFoundError,
)
from src.shared_kernel.domain.repositories import IOrganizationalUnitRepository

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class UpdateOrganizationalUnitInputDTO:
    """
    Data Transfer Object for input data when updating a existent Organizational Unit.
    """

    actor: "User"
    id: UUID
    description: str
    code: str
    parent_id: Optional[UUID] = field(default=None)


@dataclass(frozen=True)
class UpdateOrganizationalUnitOutputDTO:
    """
    Data Transfer Object for output data when updating a existent Organizational Unit.
    """

    id: UUID
    description: str


class UpdateOrganizationalUnitUseCase:
    """
    Use case for updating an existing organizational unit.
    """

    def __init__(self, repository: IOrganizationalUnitRepository) -> None:
        """
        Initialize the UpdateOrganizationalUnitUseCase.
        """

        self._repository = repository

    def execute(
        self,
        input_dto: UpdateOrganizationalUnitInputDTO,
    ) -> UpdateOrganizationalUnitOutputDTO:
        """
        Execute the use case to update an existing Organizational Unit.
        """

        entity = self._repository.get_by_id(
            entity_id=input_dto.id,
            tenant_id=input_dto.actor.tenant_id,
        )
        if not entity:
            raise OrganizationalUnitNotFoundError(
                "Organizational Unit with given ID not found"
            )

        try:
            entity.description = input_dto.description
            entity.code = input_dto.code
            entity.parent_id = input_dto.parent_id
            entity.updated_by = input_dto.actor.id
        except EntityValidationError as e:
            raise InvalidOrganizationalUnitError(f"Invalid input data: {e}") from e

        self._repository.update(entity)
        return UpdateOrganizationalUnitOutputDTO(
            id=entity.id,
            description=entity.description,
        )
