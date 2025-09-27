from dataclasses import dataclass
from uuid import UUID

from src.core.domain.entities.user import hash_password
from src.core.infrastructure.repositories import UserRepository

from .exceptions import InvalidPasswordError, UserNotFoundError


@dataclass(frozen=True)
class ChangePasswordInputDTO:
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

        user = self._repository.get_by_id(input_dto.user_id)
        if not user:
            raise UserNotFoundError("User not found.")

        if not user.verify_password(input_dto.old_password):
            raise InvalidPasswordError("Invalid old password.")

        if len(input_dto.new_password) < 8:
            raise ValueError("New password must be at least 8 characters long.")

        user.hashed_password = hash_password(input_dto.new_password)

        self._repository.update(user)
