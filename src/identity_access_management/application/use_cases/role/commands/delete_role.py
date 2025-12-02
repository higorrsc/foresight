from src.identity_access_management.application.use_cases.role import RoleNotFoundError
from src.identity_access_management.domain.entities import Role
from src.identity_access_management.domain.repositories import IRoleRepository
from src.shared_kernel.application._shared.use_cases.commands import (
    GenericDeleteUseCase,
)


class DeleteRoleUseCase(GenericDeleteUseCase[Role]):
    """
    Use case for deleting an role.
    """

    def __init__(self, repository: IRoleRepository) -> None:
        """
        Initialize the delete use case.
        """

        super().__init__(
            repository,
            RoleNotFoundError,
            "Role with given ID not found.",
        )
