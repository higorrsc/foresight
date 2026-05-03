from src.core.application.use_cases.commands import DeleteRequestInputDTO
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.exceptions import (
    InsufficientPermissionError,
    InvalidUserError,
    UserNotFoundError,
)
from src.identity_access_management.domain.repositories import IUserRepository


class DeleteUserUseCase:
    """
    Use case for deleting a user.
    """

    def __init__(self, repository: IUserRepository):
        """
        Initialize the delete user use case.
        """

        self._repository = repository

    def execute(self, input_dto: DeleteRequestInputDTO) -> None:
        """
        Execute the delete user use case.
        """

        if AppPermission.USER_DELETE not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to delete users."
            )

        user_to_delete = self._repository.get_by_id(
            entity_id=input_dto.id,
            tenant_id=input_dto.actor.tenant_id,
        )
        if not user_to_delete:
            raise UserNotFoundError("User to delete not found in this tenant.")

        if input_dto.actor.id == user_to_delete.id:
            raise InvalidUserError("User cannot delete their own account.")

        user_to_delete.soft_delete()
        user_to_delete.updated_by = input_dto.actor.id

        self._repository.update(user_to_delete)
