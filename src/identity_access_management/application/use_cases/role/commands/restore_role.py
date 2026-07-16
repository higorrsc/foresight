from src.core.application.use_cases.commands import RestoreRequestInputDTO
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.exceptions import (
    InsufficientPermissionError,
    RoleNotFoundError,
)
from src.identity_access_management.domain.repositories import IRoleRepository


class RestoreRoleUseCase:
    """
    Use case for deleting a role.
    """

    def __init__(self, repository: IRoleRepository):
        """
        Initialize the restore role use case.
        """

        self._repository = repository

    async def execute(self, input_dto: RestoreRequestInputDTO) -> None:
        """
        Execute the restore role use case.
        """

        if AppPermission.ROLE_DELETE not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to restore roles."
            )

        role_to_restore = await self._repository.get_by_id(
            entity_id=input_dto.id,
            tenant_id=input_dto.actor.tenant_id,
        )
        if not role_to_restore:
            raise RoleNotFoundError("Role to restore not found in this tenant.")

        role_to_restore.restore()
        role_to_restore.updated_by = input_dto.actor.id

        await self._repository.update(role_to_restore)
