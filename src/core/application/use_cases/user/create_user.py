from dataclasses import dataclass
from uuid import UUID

from src.core.domain._shared import AbstractRepository, EntityValidationError
from src.core.domain.entities import User, hash_password
from src.core.infrastructure.repositories import UserRepository

from .exceptions import InvalidUserError, UsernameAlreadyExistsError


@dataclass(frozen=True)
class CreateUserInputDTO:
    """
    Data Transfer Object for input data when creating a new user.
    """

    username: str
    password: str


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

    def __init__(self, repository: AbstractRepository[UserRepository]):
        """
        Constructor Initialize the CreateUserUseCase.
        """

        self._repository = repository

    def execute(self, input_dto: CreateUserInputDTO) -> CreateUserOutputDTO:
        """
        Execute the use case to create a new user.
        """

        existing_user = self._repository.get_by_username(input_dto.username)  # type: ignore
        if existing_user:
            raise UsernameAlreadyExistsError(
                f"Username '{input_dto.username}' already exists."
            )

        hashed_pwd = hash_password(input_dto.password)

        try:
            new_user = User(
                username=input_dto.username,
                hashed_password=hashed_pwd,
            )
        except EntityValidationError as e:
            raise InvalidUserError(f"Invalid user data: {e}") from e

        self._repository.save(new_user)  # type: ignore

        return CreateUserOutputDTO(
            id=new_user.id,
            username=new_user.username,
        )
