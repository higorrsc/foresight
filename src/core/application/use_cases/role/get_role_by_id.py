from src.core.application._shared.use_cases import GenericGetByIdUseCase
from src.core.application.use_cases.role import RoleNotFoundError
from src.core.domain._shared import AbstractRepository
from src.core.domain.entities import Role


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
