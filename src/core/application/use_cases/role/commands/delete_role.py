from src.core.application._shared.use_cases.commands import GenericDeleteUseCase
from src.core.application.use_cases.role import RoleNotFoundError
from src.core.domain._shared import AbstractRepository
from src.core.domain.entities import Role


class DeleteRoleUseCase(GenericDeleteUseCase[Role]):
    """
    Use case for deleting an role.
    """

    def __init__(self, repository: AbstractRepository[Role]) -> None:
        """
        Initialize the delete use case.
        """

        super().__init__(
            repository,
            RoleNotFoundError,
            "Role with given ID not found.",
        )
