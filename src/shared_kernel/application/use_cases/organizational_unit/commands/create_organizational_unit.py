from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID

from src.core.domain import EntityValidationError
from src.shared_kernel.domain.entities import OrganizationalUnit
from src.shared_kernel.domain.exceptions import InvalidOrganizationalUnitError
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
    parent_id: UUID | None = field(default=None)


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

    async def execute(
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
            entity.created_by = input_dto.actor.id
            entity.updated_by = input_dto.actor.id
        except EntityValidationError as e:
            raise InvalidOrganizationalUnitError(f"Invalid input data: {e}") from e

        await self._repository.save(entity)

        return CreateOrganizationalUnitOutputDTO(id=entity.id)
