# src/identity_access_management/application/use_cases/user/create_user.py
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List
from uuid import UUID

from src.identity_access_management.application.use_cases.role import RoleNotFoundError
from src.identity_access_management.application.use_cases.user import (
    UsernameAlreadyExistsError,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities import User
from src.identity_access_management.domain.entities.user import hash_password
from src.identity_access_management.domain.repositories import (
    IRoleRepository,
    IUserRepository,
)

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User as UserEntity


@dataclass(frozen=True)
class CreateUserInputDTO:
    """
    Data Transfer Object for input data when creating a new user
    within an existing tenant.
    """

    actor: "UserEntity"
    username: str
    password: str
    roles: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class CreateUserOutputDTO:
    """
    Data Transfer Object for output data after creating a new user.
    """

    id: UUID
    username: str


class CreateUserUseCase:
    """
    Use case for an Admin to create a new user within their Tenant.
    """

    def __init__(
        self, user_repository: IUserRepository, role_repository: IRoleRepository
    ):
        """
        Constructor for the CreateUserUseCase.
        """

        self._user_repository = user_repository
        self._role_repository = role_repository

    def execute(self, input_dto: CreateUserInputDTO) -> CreateUserOutputDTO:
        """
        Executes the use case to create a new user.
        """

        if AppPermission.USER_CREATE not in input_dto.actor.permissions:
            raise PermissionError("User does not have permission to create new users.")

        if self._user_repository.get_by_username_global(input_dto.username):
            raise UsernameAlreadyExistsError(
                f"Username '{input_dto.username}' already exists."
            )

        # 3. Validate and fetch Roles (WITHIN the actor's tenant)
        role_names_set = set(input_dto.roles)
        if not role_names_set:
            guest_role = self._role_repository.get_by_name(
                "guest",
                input_dto.actor.tenant_id,
            )
            if not guest_role:
                raise RuntimeError("Default role 'guest' not found for this tenant.")
            role_names_set = {guest_role.name}
        else:
            for role_name in role_names_set:
                if not self._role_repository.get_by_name(
                    role_name,
                    input_dto.actor.tenant_id,
                ):
                    raise RoleNotFoundError(
                        f"Role '{role_name}' not found in this tenant."
                    )

        hashed_pwd = hash_password(input_dto.password)

        new_user = User(
            username=input_dto.username,
            hashed_password=hashed_pwd,
            tenant_id=input_dto.actor.tenant_id,
            roles=role_names_set,
            is_active=True,
            created_by=input_dto.actor.id,
            updated_by=input_dto.actor.id,
        )

        self._user_repository.save(new_user)

        return CreateUserOutputDTO(
            id=new_user.id,
            username=new_user.username,
        )
