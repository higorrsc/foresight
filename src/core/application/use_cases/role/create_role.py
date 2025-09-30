from dataclasses import dataclass
from uuid import UUID

from src.core.application.use_cases.role.exceptions import InvalidRoleError
from src.core.domain._shared import AbstractRepository
from src.core.domain._shared.exceptions import EntityValidationError
from src.core.domain.entities import Role


@dataclass(frozen=True)
class CreateRoleInputDTO:
    """
    Data Transfer Object for input data when creating a new role.
    """

    name: str
    description: str


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
                description=input_dto.description,
            )
        except EntityValidationError as e:
            raise InvalidRoleError(f"Invalid input data: {e}") from e

        self._repository.save(role)
        return CreateRoleOutputDTO(id=role.id)
