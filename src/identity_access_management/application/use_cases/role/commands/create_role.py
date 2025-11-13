from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from src.identity_access_management.application.use_cases.role import InvalidRoleError
from src.identity_access_management.domain.entities import Role
from src.shared_kernel.domain._shared import AbstractRepository, EntityValidationError

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class CreateRoleInputDTO:
    """
    Data Transfer Object for input data when creating a new role.
    """

    actor: "User"
    name: str
    description: Optional[str] = None


@dataclass(frozen=True)
class CreateRoleOutputDTO:
    """
    Data Transfer Object for input data when creating a new role.
    """

    id: UUID


class CreateRoleUseCase:
    """
    Use case for creating a new role.
    """

    def __init__(self, repository: AbstractRepository[Role]):
        """
        Initialize the create use case.
        """

        self._repository = repository

    def execute(self, input_dto: CreateRoleInputDTO) -> CreateRoleOutputDTO:
        """
        Execute the use case to create a new role.
        """

        try:
            role = Role(
                name=input_dto.name,
                description=input_dto.description,  # type: ignore
                tenant_id=input_dto.actor.tenant_id,
            )
        except EntityValidationError as e:
            raise InvalidRoleError(f"Invalid input data: {e}") from e

        self._repository.save(role)
        return CreateRoleOutputDTO(id=role.id)
