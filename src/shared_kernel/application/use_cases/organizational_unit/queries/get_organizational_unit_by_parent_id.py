from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from src.shared_kernel.domain.repositories import IOrganizationalUnitRepository

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class GetOrganizationalUnitByParentIdInputDTO:
    """
    Data Transfer Object for get by id requests.
    """

    actor: "User"
    parent_id: UUID


@dataclass(frozen=True)
class GetOrganizationalUnitByParentIdOutputDTO:
    """
    Data Transfer Object for get by id requests.
    """

    id: UUID
    description: str
    code: str
    is_active: bool


class GetOrganizationalUnitByParentIdUseCase:
    """
    Use case for getting an organizational unit by its parent ID.
    """

    def __init__(self, repository: IOrganizationalUnitRepository) -> None:
        """
        Initialize the get by id use case.
        """

        self._repository = repository

    def execute(
        self,
        request: GetOrganizationalUnitByParentIdInputDTO,
    ) -> list[GetOrganizationalUnitByParentIdOutputDTO]:
        """
        Execute the get by parent id use case.
        """

        entities = self._repository.get_by_parent_id(
            parent_id=request.parent_id,
            tenant_id=request.actor.tenant_id,  # type: ignore
        )
        return (
            [
                GetOrganizationalUnitByParentIdOutputDTO(
                    id=entity.id,
                    description=entity.description,
                    code=entity.code,
                    is_active=entity.is_active,
                )
                for entity in entities
            ]
            if entities
            else []
        )
