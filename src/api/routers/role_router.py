from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from src.api.dependencies.auth import get_current_user
from src.api.dependencies.authorization import RoleChecker
from src.api.dependencies.database import get_role_repository
from src.api.routers._shared import PaginationMetaResponse
from src.core.application._shared.use_cases.commands import DeleteRequestInputDTO
from src.core.application._shared.use_cases.queries import (
    GetByIdRequestInputDTO,
    ListRequestInputDTO,
)
from src.core.application.use_cases.role import InvalidRoleError, RoleNotFoundError
from src.core.application.use_cases.role.commands import (
    CreateRoleInputDTO,
    CreateRoleUseCase,
    DeleteRoleUseCase,
    UpdateRoleRequestDTO,
    UpdateRoleUseCase,
)
from src.core.application.use_cases.role.queries import (
    GetRoleByIdUseCase,
    ListRoleUseCase,
)
from src.core.infrastructure.repositories import RoleRepository

allow_admin_only = RoleChecker(["admin"])


class RoleResponse(BaseModel):
    """
    Response model for API.
    """

    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


class RoleUpdateBody(BaseModel):
    """
    Request model for update role.
    """

    name: Optional[str] = None
    description: Optional[str] = None


class PaginatedRoleResponse(BaseModel):
    """
    Response model for API.
    """

    data: List[RoleResponse]
    meta: PaginationMetaResponse


router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    dependencies=[
        Depends(get_current_user),
        Depends(allow_admin_only),
    ],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_role_endpoint(
    request: CreateRoleInputDTO,
    repo: RoleRepository = Depends(get_role_repository),
):
    """
    Create a new role.
    """

    try:
        use_case = CreateRoleUseCase(repository=repo)
        result = use_case.execute(request)
        return {"id": result.id}
    except (ValueError, InvalidRoleError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedRoleResponse,
)
def list_routes_endpoint(
    repo: RoleRepository = Depends(get_role_repository),
    description: Optional[str] = Query(
        None,
        description="Filtrar por parte da descrição",
    ),
    sort_by: Optional[str] = Query(
        "description",
        description="Campo para ordenação",
    ),
    sort_order: str = Query(
        "asc",
        enum=["asc", "desc"],
        description="Ordem da ordenação",
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Offset para paginação",
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Limite de registos por página",
    ),
):
    """
    List roles with filters, order and pagination.
    """

    filters = {}
    if description:
        filters["description"] = description

    input_dto = ListRequestInputDTO(
        filters=filters,
        sort_by=sort_by,
        sort_order=sort_order,
        offset=offset,
        limit=limit,
    )

    use_case = ListRoleUseCase(repo)
    result = use_case.execute(input_dto)
    return result


@router.get(
    "/{role_id}",
    status_code=status.HTTP_200_OK,
    response_model=RoleResponse,
)
def get_role_by_id_endpoint(
    role_id: UUID,
    repo: RoleRepository = Depends(get_role_repository),
):
    """
    Getting a role by its ID.
    """

    try:
        use_case = GetRoleByIdUseCase(repo)
        input_dto = GetByIdRequestInputDTO(id=role_id)
        role = use_case.execute(input_dto)
        return role
    except RoleNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.patch(
    "/{role_id}",
    status_code=status.HTTP_200_OK,
)
def update_role_endpoint(
    role_id: UUID,
    request_body: RoleUpdateBody,
    repo: RoleRepository = Depends(get_role_repository),
):
    """
    Update an existing role.
    """

    try:
        use_case = UpdateRoleUseCase(repo)
        input_dto = UpdateRoleRequestDTO(
            id=role_id,
            name=request_body.name,  # type: ignore
            description=request_body.description,
        )
        output_dto = use_case.execute(input_dto)
        return {
            "id": output_dto.id,
            "name": output_dto.name,
            "description": output_dto.description,
        }
    except RoleNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_role_endpoint(
    role_id: UUID,
    repo: RoleRepository = Depends(get_role_repository),
):
    """
    Delete an existing role.
    """

    try:
        use_case = DeleteRoleUseCase(repo)
        use_case.execute(DeleteRequestInputDTO(role_id))
    except RoleNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
