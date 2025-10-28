from src.identity_access_management.domain.entities import Role
from src.shared_kernel.application._shared.use_cases.queries import GenericListUseCase
from src.shared_kernel.domain._shared import AbstractRepository


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
