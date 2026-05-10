from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.exceptions import InsufficientPermissionError
from src.tenant_management.domain.exceptions import TenantNotFoundError
from src.tenant_management.domain.repositories import ITenantRepository
from src.tenant_management.domain.value_objects import TenantStatus

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class UpdateTenantStatusInputDTO:
    """
    Data Transfer Object for input data when updating a tenant's status.
    """

    actor: "User"
    tenant_id_to_update: UUID
    new_status: TenantStatus


class UpdateTenantStatusUseCase:
    """
    Use case for updating a tenant's status.
    """

    def __init__(self, repository: ITenantRepository):
        """
        Constructor for UpdateTenantStatusUseCase.
        """

        self._repository = repository

    async def execute(self, input_dto: UpdateTenantStatusInputDTO) -> None:
        """
        Execute the use case to update a tenant's status.
        """

        if AppPermission.TENANT_UPDATE not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to update tenants."
            )

        tenant = await self._repository.get_by_id_global(input_dto.tenant_id_to_update)

        if not tenant:
            raise TenantNotFoundError("Tenant not found.")

        tenant.status = input_dto.new_status
        tenant.updated_by = input_dto.actor.id

        await self._repository.update(tenant)
