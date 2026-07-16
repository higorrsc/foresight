from dataclasses import dataclass

from src.identity_access_management.domain.entities import User
from src.identity_access_management.domain.exceptions import (
    InvalidPasswordError,
    UserNotFoundError,
)
from src.identity_access_management.domain.repositories import IUserRepository


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

    def __init__(self, repository: IUserRepository):
        """
        Initialize the AuthenticateUserUseCase.
        """

        self._repository = repository

    async def execute(self, input_dto: AuthenticateUserInputDTO) -> User:
        """
        Execute the AuthenticateUserUseCase.
        """

        user = await self._repository.get_by_username_global(input_dto.username)
        if not user:
            raise UserNotFoundError("Invalid username or password")

        if not user.is_active:
            raise UserNotFoundError("User account is inactive.")

        if not user.verify_password(input_dto.password):
            raise InvalidPasswordError("Invalid username or password")

        return user
