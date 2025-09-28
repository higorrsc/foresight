from dataclasses import dataclass

from src.core.application.use_cases.user.exceptions import UserNotFoundError
from src.core.domain.entities import User
from src.core.infrastructure.repositories import UserRepository


@dataclass(frozen=True)
class AuthenticateUserInputDTO:
    """
    Data Transfer Object for input data when authenticating a user.
    """

    username: str
    password: str


class AuthenticateUserUseCase:
    """
    Use case for authenticating a user.
    """

    def __init__(self, repository: UserRepository):
        """
        Initialize the AuthenticateUserUseCase.
        """

        self._repository = repository

    def execute(self, input_dto: AuthenticateUserInputDTO) -> User:
        """
        Execute the AuthenticateUserUseCase.
        """

        user = self._repository.get_by_username(input_dto.username)
        if not user:
            raise UserNotFoundError("Invalid username or password")

        if not user.verify_password(input_dto.password):
            raise UserNotFoundError("Invalid username or password")

        return user
