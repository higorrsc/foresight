from dataclasses import dataclass
from typing import TYPE_CHECKING, List

from src.identity_access_management.application.use_cases.user import (
    InsufficientPermissionError,
)
from src.identity_access_management.domain.constants import AppPermission
from src.tenant_management.domain.entities import Tenant
from src.tenant_management.domain.repositories import ITenantRepository

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class ListTenantsInputDTO:
    """
    Data Transfer Object for input data when listing tenants.
    """

    actor: "User"


class ListTenantsUseCase:
    """
    Use case for listing tenants.
    """

    def __init__(self, repository: ITenantRepository):
        """
        Constructor for ListTenantsUseCase.
        """

        self._repository = repository

    def execute(self, input_dto: ListTenantsInputDTO) -> List[Tenant]:
        """
        Execute the use case to list tenants.
        """

        if AppPermission.TENANT_READ not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to list tenants."
            )

        return self._repository.search(tenant_id=None).data
