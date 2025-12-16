from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict

from src.api.dependencies import get_current_user, get_permission_repository
from src.api.routers._shared import PaginatedApiResponse
from src.identity_access_management.application.use_cases.permission.queries import (
    ListPermissionsUseCase,
)
from src.identity_access_management.domain.entities import User
from src.identity_access_management.domain.repositories import IPermissionRepository
from src.shared_kernel.application._shared.use_cases.queries.generic_list import (
    ListRequestInputDTO,
)


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
def list_permissions_endpoint(
    repo: IPermissionRepository = Depends(get_permission_repository),
    actor: User = Depends(get_current_user),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Limit of records per page"),
):
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
    return use_case.execute(input_dto)
