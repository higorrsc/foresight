from src.core.application._shared.use_cases.queries import GenericListUseCase
from src.core.domain._shared import AbstractRepository
from src.core.domain.entities import Role


class ListRoleUseCase(GenericListUseCase[Role]):
    """
    Use case for listing roleRoles.
    """

    def __init__(self, repository: AbstractRepository[Role]) -> None:
        """
        Initialize the list use case.

        :param repository: The repository to use for listing roleRoles.
        """

        super().__init__(repository)
