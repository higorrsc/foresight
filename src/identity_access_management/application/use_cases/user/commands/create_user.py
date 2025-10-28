from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID

from src.identity_access_management.application.use_cases.role import InvalidRoleError
from src.identity_access_management.application.use_cases.user import (
    InvalidUserError,
    UsernameAlreadyExistsError,
)
from src.identity_access_management.domain.entities import User
from src.identity_access_management.domain.entities.user import hash_password
from src.identity_access_management.infrastructure.repositories import (
    RoleRepository,
    UserRepository,
)
from src.shared_kernel.domain._shared import EntityValidationError


@dataclass(frozen=True)
class CreateUserInputDTO:
    """
    Data Transfer Object for input data when creating a new user.
    """

    username: str
    password: str
    roles: Optional[List[str]] = field(default_factory=list)


@dataclass(frozen=True)
class CreateUserOutputDTO:
    """
    Data Transfer Object for output data when creating a new user.
    """

    id: UUID
    username: str


class CreateUserUseCase:
    """
    Use case for creating a new user.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
    ):
        """
        Constructor Initialize the CreateUserUseCase.
        """

        self._user_repository = user_repository
        self._role_repository = role_repository

    def execute(self, input_dto: CreateUserInputDTO) -> CreateUserOutputDTO:
        """
        Execute the use case to create a new user.
        """

        existing_user = self._user_repository.get_by_username(input_dto.username)  # type: ignore
        if existing_user:
            raise UsernameAlreadyExistsError(
                f"Username '{input_dto.username}' already exists."
            )

        hashed_pwd = hash_password(input_dto.password)

        role_names = set(input_dto.roles) if input_dto.roles else set()
        if role_names:
            for role in role_names:
                if not self._role_repository.get_by_name(role):
                    raise InvalidRoleError(f"Role '{role}' does not exist.")
        else:
            guest_role = self._role_repository.get_by_name("guest")
            if not guest_role:
                raise RuntimeError("Default role 'guest' not found in the system.")
            role_names.add(guest_role.name)

        try:
            new_user = User(
                username=input_dto.username,
                hashed_password=hashed_pwd,
                roles=role_names,
            )
        except EntityValidationError as e:
            raise InvalidUserError(f"Invalid user data: {e}") from e

        self._user_repository.save(new_user)  # type: ignore

        return CreateUserOutputDTO(
            id=new_user.id,
            username=new_user.username,
        )
