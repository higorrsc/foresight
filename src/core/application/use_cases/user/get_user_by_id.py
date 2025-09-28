from src.core.application._shared.use_cases import GenericGetByIdUseCase
from src.core.application.use_cases.user import UserNotFoundError
from src.core.domain._shared import AbstractRepository
from src.core.domain.entities import User


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
