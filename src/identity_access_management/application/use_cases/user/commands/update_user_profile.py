from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from src.identity_access_management.application.use_cases.user import (
    InsufficientPermissionError,
    InvalidUserError,
    UserNotFoundError,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.infrastructure.repositories import UserRepository
from src.shared_kernel.domain._shared import EntityValidationError

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class UserProfileRequestDTO:
    """
    Data Transfer Object for input data when getting a user's profile.
    """

    actor: "User"
    user_id_to_update: UUID
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

        is_self_update = input_dto.actor.id == input_dto.user_id_to_update
        can_update_others = AppPermission.USER_UPDATE in input_dto.actor.permissions

        if not is_self_update and not can_update_others:
            raise InsufficientPermissionError(
                "User does not have permission to update another user's profile."
            )

        user_to_update = self._repository.get_by_id(
            entity_id=input_dto.user_id_to_update,
            tenant_id=input_dto.actor.tenant_id,
        )
        if not user_to_update:
            raise UserNotFoundError(
                f"User with id '{input_dto.user_id_to_update}' not found."
            )

        something_changed = False

        if input_dto.first_name is not None:
            user_to_update.first_name = input_dto.first_name
            something_changed = True

        if input_dto.last_name is not None:
            user_to_update.last_name = input_dto.last_name
            something_changed = True

        if input_dto.email is not None:
            user_to_update.email = input_dto.email
            something_changed = True

        if input_dto.is_active is not None:
            if (
                not can_update_others
                and input_dto.is_active != user_to_update.is_active
            ):
                raise InsufficientPermissionError(
                    "User does not have permission to change 'is_active' status."
                )
            user_to_update.is_active = input_dto.is_active
            something_changed = True

        if not something_changed:
            return

        try:
            user_to_update.updated_by = input_dto.actor.id
            user_to_update.validate()
        except EntityValidationError as e:
            raise InvalidUserError(f"Invalid user data: {e}") from e

        self._repository.update(user_to_update)
