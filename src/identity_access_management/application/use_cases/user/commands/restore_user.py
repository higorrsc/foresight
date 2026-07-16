from src.core.application.use_cases.commands import RestoreRequestInputDTO
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.exceptions import (
    InsufficientPermissionError,
    InvalidUserError,
    UserNotFoundError,
)
from src.identity_access_management.domain.repositories import IUserRepository


class RestoreUserUseCase:
    """
    Use case for deleting a user.
    """

    def __init__(self, repository: IUserRepository):
        """
        Initialize the restore user use case.
        """

        self._repository = repository

    async def execute(self, input_dto: RestoreRequestInputDTO) -> None:
        """
        Execute the restore user use case.
        """

        if AppPermission.USER_DELETE not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to restore users."
            )

        user_to_restore = await self._repository.get_by_id(
            entity_id=input_dto.id,
            tenant_id=input_dto.actor.tenant_id,
        )
        if not user_to_restore:
            raise UserNotFoundError("User to restore not found in this tenant.")

        if input_dto.actor.id == user_to_restore.id:
            raise InvalidUserError("User cannot restore their own account.")

        user_to_restore.restore()
        user_to_restore.updated_by = input_dto.actor.id

        await self._repository.update(user_to_restore)
