from src.core.application.use_cases.commands import DeleteRequestInputDTO
from src.identity_access_management.domain.constants.permissions import AppPermission
from src.identity_access_management.domain.exceptions import (
    InsufficientPermissionError,
    RoleDeletionIntegrityError,
    RoleNotFoundError,
)
from src.identity_access_management.domain.repositories import (
    IRoleRepository,
    IUserRepository,
)


class DeleteRoleUseCase:
    """
    Use case for deleting an role.
    """

    def __init__(
        self,
        role_repository: IRoleRepository,
        user_repository: IUserRepository,
    ) -> None:
        """
        Initialize the delete use case.
        """

        self._role_repository = role_repository
        self._user_repository = user_repository

    async def execute(self, input_dto: DeleteRequestInputDTO) -> None:
        """
        Execute the delete use case.
        """

        if AppPermission.ROLE_DELETE not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to set permissions."
            )

        role_to_delete = await self._role_repository.get_by_id(
            input_dto.id,
            input_dto.actor.tenant_id,
        )

        if not role_to_delete:
            raise RoleNotFoundError(f"Role with ID '{input_dto.id}' not found.")

        users_count = await self._user_repository.count_users_by_role(role_to_delete.id)

        if users_count > 0:
            raise RoleDeletionIntegrityError(
                f"Cannot delete role '{role_to_delete.name}' "
                f"because it is assigned to {users_count} users."
            )

        role_to_delete.soft_delete()
        role_to_delete.updated_by = input_dto.actor.id

        await self._role_repository.update(role_to_delete)
