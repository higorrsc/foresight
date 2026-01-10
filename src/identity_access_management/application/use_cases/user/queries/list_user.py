from src.core.application.use_cases.queries import GenericListUseCase
from src.core.domain.repository import AbstractRepository
from src.identity_access_management.domain.entities import User


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
