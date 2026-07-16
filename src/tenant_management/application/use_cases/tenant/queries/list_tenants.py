from dataclasses import dataclass
from math import ceil
from typing import TYPE_CHECKING, Any

from src.core.application.dto import PaginatedResponseDTO, PaginationMeta
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.exceptions import InsufficientPermissionError
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
    filters: dict[str, Any] | None = None
    sort_by: str | None = None
    sort_order: str = "asc"
    offset: int = 0
    limit: int = 10


class ListTenantsUseCase:
    """
    Use case for listing tenants.
    """

    def __init__(self, repository: ITenantRepository):
        """
        Constructor for ListTenantsUseCase.
        """

        self._repository = repository

    async def execute(
        self, input_dto: ListTenantsInputDTO
    ) -> PaginatedResponseDTO[Tenant]:
        """
        Execute the use case to list tenants.
        """

        if AppPermission.TENANT_READ not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to list tenants."
            )

        paginated_result = await self._repository.search(
            tenant_id=None,  # <-- Força None porque Plan é global
            filters=input_dto.filters,
            sort_by=input_dto.sort_by,
            sort_order=input_dto.sort_order,
            offset=input_dto.offset,
            limit=input_dto.limit,
        )

        total_items = paginated_result.total
        page_size = input_dto.limit

        if page_size > 0:
            total_pages = ceil(total_items / page_size)
            current_page = (input_dto.offset // page_size) + 1
        else:
            total_pages = 0
            current_page = 1

        return PaginatedResponseDTO(
            data=paginated_result.data,
            meta=PaginationMeta(
                total_items=total_items,
                current_page=current_page,
                page_size=page_size,
                total_pages=total_pages,
            ),
        )
