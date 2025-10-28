from src.identity_access_management.application.use_cases.user import UserNotFoundError
from src.identity_access_management.domain.entities import User
from src.shared_kernel.application._shared.use_cases.queries import (
    GenericGetByIdUseCase,
)
from src.shared_kernel.domain._shared import AbstractRepository


class GetUserByIdUseCase(GenericGetByIdUseCase[User]):
    """
    Use case for getting a user by its ID.
    """

    def __init__(self, repository: AbstractRepository[User]) -> None:
        """
        Initialize the get by id use case.
        """

        super().__init__(
            repository,
            UserNotFoundError,
            "User with given ID not found.",
        )
