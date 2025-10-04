from dataclasses import dataclass
from typing import List
from uuid import UUID

from src.core.application.use_cases.user import UserNotFoundError
from src.core.infrastructure.repositories import RoleRepository, UserRepository


@dataclass
class SetUserRolesRequestDTO:
    """
    Data Transfer Object for input data when setting user roles.
    """

    user_id: UUID
    role_names: List[str]


class SetUserRolesUseCase:
    """
    Use case for setting user roles.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
    ):
        """
        Constructor Initialize the SetUserRolesUseCase.
        """

        self._user_repository = user_repository
        self._role_repository = role_repository

    def execute(self, input_dto: SetUserRolesRequestDTO) -> None:
        """
        Execute the use case to set user roles.
        """

        user = self._user_repository.get_by_id(input_dto.user_id)
        if not user:
            raise UserNotFoundError(f"User with ID '{input_dto.user_id}' not found.")

        role_names_set = set(input_dto.role_names)
        for role_name in role_names_set:
            if not self._role_repository.get_by_name(role_name):
                raise ValueError(f"Role '{role_name}' does not exist.")

        user.roles = role_names_set
        self._user_repository.update(user)
