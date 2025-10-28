from src.identity_access_management.domain.entities import User
from src.shared_kernel.application._shared.use_cases.queries import GenericListUseCase
from src.shared_kernel.domain._shared import AbstractRepository


class ListUserUseCase(GenericListUseCase[User]):
    """
    Use case to list users.
    """

    def __init__(self, repository: AbstractRepository[User]) -> None:
        """
        Initialize the ListUserUseCase.

        :param repository: The repository to use for listing users.
        """

        super().__init__(repository)
