from dataclasses import dataclass
from typing import TYPE_CHECKING, List

from src.identity_access_management.domain.entities import Permission
from src.identity_access_management.domain.repositories import IPermissionRepository

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class ListPermissionsInputDTO:
    """
    Input DTO for listing permissions.
    """

    actor: "User"


class ListPermissionsUseCase:
    """
    Use case to list all available system permissions.
    Usually restricted do Admins or users who can manage roles.
    """

    def __init__(self, repository: IPermissionRepository):
        """
        Initialize the use case.

        :param repository: The repository to use for listing permissions.
        """

        self._repository = repository

    def execute(self, input_dto: ListPermissionsInputDTO) -> List[Permission]:
        """
        Execute the use case.

        :param input_dto: The input DTO for the use case.
        :return: A list of permissions.
        """

        return self._repository.list_all()
