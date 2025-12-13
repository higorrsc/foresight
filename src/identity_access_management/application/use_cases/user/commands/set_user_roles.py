from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List
from uuid import UUID

from src.identity_access_management.application.use_cases.permission import (
    InsufficientPermissionError,
)
from src.identity_access_management.application.use_cases.role import RoleNotFoundError
from src.identity_access_management.application.use_cases.user import UserNotFoundError
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.repositories import (
    IRoleRepository,
    IUserRepository,
)

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass
class SetUserRolesInputDTO:
    """
    Data Transfer Object for input data when setting user roles.
    """

    actor: "User"
    user_id_to_update: UUID
    role_names: List[str] = field(default_factory=list)


class SetUserRolesUseCase:
    """
    Use case for setting user roles.
    """

    def __init__(
        self,
        user_repository: IUserRepository,
        role_repository: IRoleRepository,
    ):
        """
        Constructor Initialize the SetUserRolesUseCase.
        """

        self._user_repository = user_repository
        self._role_repository = role_repository

    def execute(self, input_dto: SetUserRolesInputDTO) -> None:
        """
        Execute the use case to set user roles.
        """
        if AppPermission.USER_SET_ROLES not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to set roles."
            )

        user_to_update = self._user_repository.get_by_id(
            input_dto.user_id_to_update,
            input_dto.actor.tenant_id,
        )
        if not user_to_update:
            raise UserNotFoundError(
                f"User with ID '{input_dto.user_id_to_update}' not found."
            )

        valid_roles = []
        role_names_set = set(input_dto.role_names)

        if role_names_set:
            for role_name in role_names_set:
                role = self._role_repository.get_by_name(
                    role_name,
                    input_dto.actor.tenant_id,
                )
                if not role:
                    raise RoleNotFoundError(f"Role '{role_name}' not found.")

                valid_roles.append(role)

        user_to_update.roles = {role.name for role in valid_roles}
        user_to_update.updated_by = input_dto.actor.id
        self._user_repository.update(user_to_update)
