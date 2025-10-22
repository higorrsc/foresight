from src.core.application._shared.use_cases.queries import GenericListUseCase
from src.core.domain._shared import AbstractRepository
from src.core.domain.entities import User


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
