from src.identity_access_management.application.use_cases.role import RoleNotFoundError
from src.identity_access_management.domain.entities import Role
from src.shared_kernel.application._shared.use_cases.queries import (
    GenericGetByIdUseCase,
)
from src.shared_kernel.domain._shared import AbstractRepository


class GetRoleByIdUseCase(GenericGetByIdUseCase[Role]):
    """
    Use case for getting a role by its ID.
    """

    def __init__(self, repository: AbstractRepository[Role]) -> None:
        """
        Initialize the get by id use case.
        """

        super().__init__(
            repository,
            RoleNotFoundError,
            "Role with given ID not found.",
        )
