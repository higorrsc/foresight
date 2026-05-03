from src.core.application.use_cases.queries import GetByIdRequestInputDTO
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities import User
from src.identity_access_management.domain.exceptions import (
    InsufficientPermissionError,
    UserNotFoundError,
)
from src.identity_access_management.domain.repositories import IUserRepository


class GetUserByIdUseCase:
    """
    Use case to get a user by id.
    """

    def __init__(self, repository: IUserRepository):
        """
        Initialize the GetUserByIdUseCase.

        :param user_repository: The repository to use for getting users.
        """

        self._repository = repository

    def execute(self, input_dto: GetByIdRequestInputDTO) -> User:
        """
        Execute the GetUserByIdUseCase.

        :param input_dto: The input data transfer object.
        :return: The user
        """

        if AppPermission.USER_READ not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to read user data."
            )

        user = self._repository.get_by_id(
            input_dto.id,
            tenant_id=input_dto.actor.tenant_id,
        )

        if not user:
            raise UserNotFoundError(
                f"User with id={input_dto.id} not found in this tenant."
            )

        return user
