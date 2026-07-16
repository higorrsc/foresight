from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from src.identity_access_management.domain.constants.permissions import AppPermission
from src.identity_access_management.domain.entities.user import hash_password
from src.identity_access_management.domain.exceptions import (
    InsufficientPermissionError,
    InvalidPasswordError,
    UserNotFoundError,
)
from src.identity_access_management.domain.repositories import IUserRepository

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class ChangePasswordInputDTO:
    """
    Data Transfer Object for input data when changing a user's password.
    """

    actor: "User"
    user_id_to_change: UUID
    old_password: str
    new_password: str


class ChangePasswordUseCase:
    """
    UseCase to change a user's password.
    """

    def __init__(self, repository: IUserRepository):
        """
        Initialize the ChangePasswordUseCase.
        """

        self._repository = repository

    async def execute(self, input_dto: ChangePasswordInputDTO) -> None:
        """
        Execute the ChangePasswordUseCase.
        """

        is_self_change = input_dto.actor.id == input_dto.user_id_to_change
        can_change_others = AppPermission.USER_UPDATE in input_dto.actor.permissions

        if not is_self_change and not can_change_others:
            raise InsufficientPermissionError(
                "User does not have permission to change another user's password."
            )

        user_to_update = await self._repository.get_by_id(
            input_dto.user_id_to_change,
            input_dto.actor.tenant_id,
        )

        if not user_to_update:
            raise UserNotFoundError(
                f"User with ID '{input_dto.user_id_to_change}' not found."
            )

        if is_self_change:
            if not user_to_update.verify_password(input_dto.old_password):
                raise InvalidPasswordError("Invalid old password.")

        if len(input_dto.new_password) < 8:
            raise ValueError("New password must be at least 8 characters long.")

        user_to_update.hashed_password = hash_password(input_dto.new_password)
        user_to_update.updated_by = input_dto.actor.id

        await self._repository.update(user_to_update)
