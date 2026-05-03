from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID

from src.core.domain import EntityValidationError
from src.identity_access_management.domain.entities import Role
from src.identity_access_management.domain.exceptions import (
    InvalidRoleError,
    PermissionNotFoundError,
)
from src.identity_access_management.domain.repositories import (
    IPermissionRepository,
    IRoleRepository,
)

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class CreateRoleInputDTO:
    """
    Data Transfer Object for input data when creating a new role.
    """

    actor: "User"
    name: str
    description: str | None = None
    permissions: list[str] = field(default_factory=list)


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

    def __init__(
        self,
        role_repository: IRoleRepository,
        permission_repository: IPermissionRepository,
    ):
        """
        Initialize the create use case.
        """

        self._role_repository = role_repository
        self._permission_repository = permission_repository

    def execute(self, input_dto: CreateRoleInputDTO) -> CreateRoleOutputDTO:
        """
        Execute the use case to create a new role.
        """

        try:
            permission_codes_set = set(input_dto.permissions)
            for permission_code in permission_codes_set:
                if not self._permission_repository.get_by_codename(
                    permission_code,
                ):
                    raise PermissionNotFoundError(
                        f"Permission '{permission_code}' not found."
                    )

            role = Role(
                name=input_dto.name,
                description=input_dto.description,  # type: ignore
                permissions=permission_codes_set,
                tenant_id=input_dto.actor.tenant_id,
            )
        except EntityValidationError as e:
            raise InvalidRoleError(f"Invalid input data: {e}") from e

        self._role_repository.save(role)
        return CreateRoleOutputDTO(id=role.id)
