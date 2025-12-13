from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List
from uuid import UUID

from src.identity_access_management.application.use_cases.permission import (
    InsufficientPermissionError,
    PermissionNotFoundError,
)
from src.identity_access_management.application.use_cases.role import RoleNotFoundError
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.repositories import (
    IPermissionRepository,
    IRoleRepository,
)

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass
class SetRolePermissionsInputDTO:
    """
    Data Transfer Object for input data when setting role permissions.
    """

    actor: "User"
    role_id_to_update: UUID
    permissions_codes: List[str] = field(default_factory=list)


class SetRolePermissionsUseCase:
    """
    Use case for setting role permissions.
    """

    def __init__(
        self,
        role_repository: IRoleRepository,
        permission_repository: IPermissionRepository,
    ):
        """
        Constructor Initialize the SetRolePermissionsUseCase.
        """

        self._role_repository = role_repository
        self._permission_repository = permission_repository

    def execute(self, input_dto: SetRolePermissionsInputDTO) -> None:
        """
        Execute the use case to set role permissions.
        """
        if AppPermission.ROLE_SET_PERMISSIONS not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to set permissions."
            )

        role_to_update = self._role_repository.get_by_id(
            input_dto.role_id_to_update,
            input_dto.actor.tenant_id,
        )
        if not role_to_update:
            raise RoleNotFoundError(
                f"Role with ID '{input_dto.role_id_to_update}' not found."
            )

        valid_permissions = []
        permissions_codes_set = set(input_dto.permissions_codes)

        if permissions_codes_set:
            for permission_code in permissions_codes_set:
                permission = self._permission_repository.get_by_codename(
                    permission_code,
                )
                if not permission:
                    raise PermissionNotFoundError(
                        f"Permission '{permission_code}' does not exist."
                    )

                valid_permissions.append(permission)

        role_to_update.permissions = {
            permission.codename for permission in valid_permissions
        }
        role_to_update.updated_by = input_dto.actor.id
        self._role_repository.update(role_to_update)
