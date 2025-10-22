from src.core.application._shared.use_cases.commands import GenericRestoreUseCase
from src.core.application.use_cases.user import UserNotFoundError
from src.core.domain._shared.repository import AbstractRepository
from src.core.domain.entities import User


class RestoreUserUseCase(GenericRestoreUseCase[User]):
    """
    Use case for deleting an user.
    """

    def __init__(self, repository: AbstractRepository[User]) -> None:
        """
        Initialize the restore use case.
        """

        super().__init__(
            repository,
            UserNotFoundError,
            "User with given ID not found.",
        )
