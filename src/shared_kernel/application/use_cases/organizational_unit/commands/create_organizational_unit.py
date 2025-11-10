from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from src.shared_kernel.application.use_cases.organizational_unit import (
    InvalidOrganizationalUnitError,
)
from src.shared_kernel.domain._shared import EntityValidationError
from src.shared_kernel.domain.entities import OrganizationalUnit
from src.shared_kernel.domain.repositories import IOrganizationalUnitRepository

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class CreateOrganizationalUnitInputDTO:
    """
    Data Transfer Object for input data when creating a new Organizational Unit.
    """

    actor: "User"
    description: str
    code: str
    parent_id: Optional[UUID] = field(default=None)


@dataclass(frozen=True)
class CreateOrganizationalUnitOutputDTO:
    """
    Data Transfer Object for output data when creating a new Organizational Unit.
    """

    id: UUID


class CreateOrganizationalUnitUseCase:
    """
    Create a new OrganizationalUnit.
    """

    def __init__(self, repository: IOrganizationalUnitRepository) -> None:
        """
        Initialize the CreateOrganizationalUnitUseCase.
        """

        self._repository = repository

    def execute(
        self,
        input_dto: CreateOrganizationalUnitInputDTO,
    ) -> CreateOrganizationalUnitOutputDTO:
        """
        Execute the use case to create a new Organizational Unit.
        """

        try:
            entity = OrganizationalUnit(
                description=input_dto.description,
                code=input_dto.code,
                parent_id=input_dto.parent_id,
                tenant_id=input_dto.actor.tenant_id,
            )
        except EntityValidationError as e:
            raise InvalidOrganizationalUnitError(f"Invalid input data: {e}") from e

        self._repository.save(entity)
        return CreateOrganizationalUnitOutputDTO(id=entity.id)
