from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.identity_access_management.application.use_cases.role import (
    InvalidRoleError,
    RoleNotFoundError,
)
from src.identity_access_management.domain.entities import Role
from src.shared_kernel.domain._shared import AbstractRepository, EntityValidationError


@dataclass
class UpdateRoleRequestDTO:
    """
    Data Transfer Object for input data when updating a role.
    """

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

    def __init__(self, repository: AbstractRepository[Role]) -> None:
        """
        Initialize the update use case.
        """

        self._repository = repository

    def execute(self, input_dto: UpdateRoleRequestDTO) -> UpdateRoleResponseDTO:
        """
        Execute the use case to update a role.
        """

        role = self._repository.get_by_id(input_dto.id)
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
