from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from src.identity_access_management.application.use_cases.user import (
    InvalidPasswordError,
    UserNotFoundError,
)
from src.identity_access_management.domain.entities.user import hash_password
from src.identity_access_management.infrastructure.repositories import UserRepository

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class ChangePasswordInputDTO:
    """
    Data Transfer Object for input data when changing a user's password.
    """

    actor: "User"
    user_id: UUID
    old_password: str
    new_password: str


class ChangePasswordUseCase:
    """
    UseCase to change a user's password.
    """

    def __init__(self, repository: UserRepository):
        """
        Initialize the ChangePasswordUseCase.
        """

        self._repository = repository

    def execute(self, input_dto: ChangePasswordInputDTO) -> None:
        """
        Execute the ChangePasswordUseCase.
        """

        user = self._repository.get_by_id(
            input_dto.user_id,
            input_dto.actor.tenant_id,
        )
        if not user:
            raise UserNotFoundError(f"User with ID '{input_dto.user_id}' not found.")

        if not user.verify_password(input_dto.old_password):
            raise InvalidPasswordError("Invalid old password.")

        if len(input_dto.new_password) < 8:
            raise ValueError("New password must be at least 8 characters long.")

        user.hashed_password = hash_password(input_dto.new_password)

        self._repository.update(user)
