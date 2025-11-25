from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict

from src.api.dependencies.auth import get_current_user
from src.api.dependencies.database import get_permission_repository
from src.api.routers._shared import PaginatedApiResponse
from src.identity_access_management.application.use_cases.permission.queries import (
    ListPermissionsInputDTO,
    ListPermissionsUseCase,
)
from src.identity_access_management.domain.entities import User
from src.identity_access_management.infrastructure.repositories import (
    PermissionRepository,
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
    response_model=List[PermissionResponse],
)
def list_permissions_endpoint(
    repo: PermissionRepository = Depends(get_permission_repository),
    actor: User = Depends(get_current_user),
):
    """
    List all available system permissions.
    Useful for frontend interfaces when creating/editing Roles.
    """

    use_case = ListPermissionsUseCase(repo)
    input_dto = ListPermissionsInputDTO(actor)
    permissions = use_case.execute(input_dto)

    return permissions
