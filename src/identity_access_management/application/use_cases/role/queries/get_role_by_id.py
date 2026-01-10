from src.core.application.use_cases.queries import GenericGetByIdUseCase
from src.identity_access_management.application.use_cases.role import RoleNotFoundError
from src.identity_access_management.domain.entities import Role
from src.identity_access_management.domain.repositories import IRoleRepository


class GetRoleByIdUseCase(GenericGetByIdUseCase[Role]):
    """
    Use case for getting a role by its ID.
    """

    def __init__(self, repository: IRoleRepository) -> None:
        """
        Initialize the get by id use case.
        """

        super().__init__(
            repository,
            RoleNotFoundError,
            "Role with given ID not found.",
        )
