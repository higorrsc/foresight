from src.identity_access_management.application.use_cases.user import UserNotFoundError
from src.identity_access_management.domain.entities import User
from src.shared_kernel.application._shared.use_cases.commands import (
    GenericRestoreUseCase,
)
from src.shared_kernel.domain._shared import AbstractRepository


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
