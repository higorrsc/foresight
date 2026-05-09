from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID

from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.exceptions import (
    InsufficientPermissionError,
    PermissionNotFoundError,
    UserNotFoundError,
)
from src.identity_access_management.domain.repositories import (
    IPermissionRepository,
    IUserRepository,
)

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass
class SetUserPermissionsInputDTO:
    """
    Data Transfer Object for input data when setting user permissions.
    """

    actor: "User"
    user_id_to_update: UUID
    permissions_codes: list[str] = field(default_factory=list)


class SetUserPermissionsUseCase:
    """
    Use case for setting user permissions.
    """

    def __init__(
        self,
        user_repository: IUserRepository,
        permission_repository: IPermissionRepository,
    ):
        """
        Constructor Initialize the SetUserPermissionsUseCase.
        """

        self._user_repository = user_repository
        self._permission_repository = permission_repository

    async def execute(self, input_dto: SetUserPermissionsInputDTO) -> None:
        """
        Execute the use case to set user permissions.
        """
        if AppPermission.USER_SET_PERMISSIONS not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to set permissions."
            )

        user_to_update = await self._user_repository.get_by_id(
            input_dto.user_id_to_update,
            input_dto.actor.tenant_id,
        )
        if not user_to_update:
            raise UserNotFoundError(
                f"User with ID '{input_dto.user_id_to_update}' not found."
            )

        valid_permissions = []
        permissions_codes_set = set(input_dto.permissions_codes)

        if permissions_codes_set:
            for permission_code in permissions_codes_set:
                permission = await self._permission_repository.get_by_codename(
                    permission_code,
                )
                if not permission:
                    raise PermissionNotFoundError(
                        f"Permission '{permission_code}' not found."
                    )

                valid_permissions.append(permission)

        user_to_update.permissions = {
            permission.codename for permission in valid_permissions
        }
        user_to_update.updated_by = input_dto.actor.id

        await self._user_repository.update(user_to_update)
