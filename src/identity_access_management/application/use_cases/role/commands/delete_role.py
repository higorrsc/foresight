from src.identity_access_management.application.use_cases.role import RoleNotFoundError
from src.identity_access_management.domain.entities import Role
from src.shared_kernel.application._shared.use_cases.commands import (
    GenericDeleteUseCase,
)
from src.shared_kernel.domain._shared import AbstractRepository


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
