from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from src.core.domain import EntityValidationError
from src.identity_access_management.application.use_cases.role import (
    InvalidRoleError,
    RoleNotFoundError,
)
from src.identity_access_management.domain.repositories import IRoleRepository

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass
class UpdateRoleInputDTO:
    """
    Data Transfer Object for input data when updating a role.
    """

    actor: "User"
    id: UUID
    name: str
    description: Optional[str] = None


@dataclass
class UpdateRoleResponseDTO:
    """
    Data Transfer Object for output data when updating a role.
    """

    id: UUID
    name: str
    description: Optional[str]


class UpdateRoleUseCase:
    """
    Use case for updating a role.
    """

    def __init__(self, repository: IRoleRepository) -> None:
        """
        Initialize the update use case.
        """

        self._repository = repository

    def execute(self, input_dto: UpdateRoleInputDTO) -> UpdateRoleResponseDTO:
        """
        Execute the use case to update a role.
        """

        role = self._repository.get_by_id(
            input_dto.id,
            input_dto.actor.tenant_id,
        )
        if role is None:
            raise RoleNotFoundError(f"Role with id {input_dto.id} not found.")

        try:
            if not input_dto.name:
                role.update_role(
                    new_name=role.name,
                    new_description=input_dto.description,
                )
            else:
                role.update_role(
                    new_name=input_dto.name,
                    new_description=input_dto.description,
                )
        except EntityValidationError as e:
            raise InvalidRoleError(f"Invalid input data: {e}") from e

        self._repository.update(role)

        return UpdateRoleResponseDTO(
            id=role.id,
            name=role.name,
            description=role.description,
        )
