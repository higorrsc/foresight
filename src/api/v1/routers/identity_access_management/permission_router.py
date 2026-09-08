from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict

from src.api.dependencies import (
    CurrentUserDep,
    PermissionRepositoryDep,
    get_current_user,
)
from src.api.v1.routers._shared import PaginatedApiResponse
from src.core.application import PaginatedResponseDTO
from src.core.application.use_cases.queries.generic_list import ListRequestInputDTO
from src.identity_access_management.application.use_cases.permission.queries import (
    ListPermissionsUseCase,
)
from src.identity_access_management.domain.entities import Permission


class PermissionResponse(BaseModel):
    """
    Response model for Permission API
    """

    id: UUID
    codename: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class PaginatedPermissionResponse(PaginatedApiResponse[PermissionResponse]):
    """
    Paginated response model for Permission.
    """


router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedPermissionResponse,
)
async def list_permissions_endpoint(
    repo: PermissionRepositoryDep,
    actor: CurrentUserDep,
    offset: Annotated[int, Query(ge=0, description="Offset for pagination")] = 0,
    limit: Annotated[
        int, Query(ge=1, le=100, description="Limit of records per page")
    ] = 10,
) -> PaginatedResponseDTO[Permission]:
    """
    List all available system permissions.
    Useful for frontend interfaces when creating/editing Roles.
    """

    input_dto = ListRequestInputDTO(
        actor=actor,
        offset=offset,
        limit=limit,
    )

    use_case = ListPermissionsUseCase(repo)
    return await use_case.execute(input_dto)
