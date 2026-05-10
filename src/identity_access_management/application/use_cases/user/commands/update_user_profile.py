from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from src.core.domain import EntityValidationError
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.exceptions import (
    InsufficientPermissionError,
    InvalidUserError,
    UserNotFoundError,
)
from src.identity_access_management.domain.repositories import IUserRepository

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class UserProfileInputDTO:
    """
    Data Transfer Object for input data when getting a user's profile.
    """

    actor: "User"
    user_id_to_update: UUID
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None


class UpdateUserProfileUseCase:
    """
    Use Case for updating a user's profile.
    """

    def __init__(self, repository: IUserRepository):
        """
        Initialize the UpdateUserProfileUseCase.
        """

        self._repository = repository

    async def execute(
        self,
        input_dto: UserProfileInputDTO,
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

        user_to_update = await self._repository.get_by_id(
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

        if not something_changed:
            return

        try:
            user_to_update.updated_by = input_dto.actor.id
            user_to_update.validate()
        except EntityValidationError as e:
            raise InvalidUserError(f"Invalid user data: {e}") from e

        await self._repository.update(user_to_update)
