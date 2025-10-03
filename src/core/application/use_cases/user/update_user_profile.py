from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.core.application.use_cases.user import InvalidUserError, UserNotFoundError
from src.core.domain._shared import EntityValidationError
from src.core.infrastructure.repositories import UserRepository


@dataclass(frozen=True)
class UserProfileRequestDTO:
    """
    Data Transfer Object for input data when getting a user's profile.
    """

    user_id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


class UpdateUserProfileUseCase:
    """
    Use Case for updating a user's profile.
    """

    def __init__(self, repository: UserRepository):
        """
        Initialize the UpdateUserProfileUseCase.
        """

        self._repository = repository

    def execute(
        self,
        input_dto: UserProfileRequestDTO,
    ) -> None:
        """
        Execute the UpdateUserProfileUseCase.
        """

        user = self._repository.get_by_id(input_dto.user_id)  # type: ignore
        if not user:
            raise UserNotFoundError(f"User with id '{input_dto.user_id}' not found.")

        if input_dto.first_name is not None:
            user.first_name = input_dto.first_name

        if input_dto.last_name is not None:
            user.last_name = input_dto.last_name

        if input_dto.email is not None:
            user.email = input_dto.email

        if input_dto.is_active is not None:
            user.is_active = input_dto.is_active

        try:
            user._validate()
        except EntityValidationError as e:
            raise InvalidUserError(f"Invalid user data: {e}") from e

        self._repository.update(user)
