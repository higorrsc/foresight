from src.core.application.use_cases.queries import GenericListUseCase
from src.identity_access_management.domain.entities import Role
from src.identity_access_management.domain.repositories import IRoleRepository


class ListRoleUseCase(GenericListUseCase[Role]):
    """
    Use case for listing roleRoles.
    """

    def __init__(self, repository: IRoleRepository) -> None:
        """
        Initialize the list use case.

        :param repository: The repository to use for listing roleRoles.
        """

        super().__init__(repository)
