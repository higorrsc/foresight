from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict, Field

from src.api.dependencies import (
    PermissionChecker,
    get_current_user,
    get_scenario_repository,
)
from src.api.routers._shared import PaginatedApiResponse
from src.core.application.use_cases.commands.generic_delete import DeleteRequestInputDTO
from src.core.application.use_cases.commands.generic_restore import (
    RestoreRequestInputDTO,
)
from src.core.application.use_cases.queries import (
    GetByIdRequestInputDTO,
    ListRequestInputDTO,
)
from src.identity_access_management.domain.entities import User
from src.planning.application.use_cases.scenario.commands import (
    CreateScenarioInputDTO,
    CreateScenarioUseCase,
    DeleteScenarioUseCase,
    LockScenarioInputDTO,
    LockScenarioUseCase,
    RestoreScenarioUseCase,
    UnlockScenarioInputDTO,
    UnlockScenarioUseCase,
    UpdateScenarioInputDTO,
    UpdateScenarioUseCase,
)
from src.planning.application.use_cases.scenario.queries import (
    GetScenarioByIdUseCase,
    ListScenarioUseCase,
)
from src.planning.domain.entities.scenario import ScenarioType
from src.planning.domain.exceptions import (
    InvalidScenarioError,
    ScenarioAlreadyLockedError,
    ScenarioAlreadyUnlockedError,
    ScenarioNotFoundError,
)
from src.planning.domain.repositories import IScenarioRepository

# --- Permissions ---
require_financial_scenario_create_or_update = PermissionChecker(
    [
        "financial_scenario:create",
        "financial_scenario:update",
    ]
)
require_financial_scenario_delete = PermissionChecker(
    [
        "financial_scenario:delete",
    ]
)
require_financial_scenario_read = PermissionChecker(
    [
        "financial_scenario:read",
    ]
)


# --- Response Models ---
class ScenarioDetailResponse(BaseModel):
    """
    Response model for Scenario API.
    """

    id: UUID
    description: str
    scenario_type: str
    is_locked: bool = False
    assumptions: str | None
    created_by: UUID
    created_at: datetime
    updated_by: UUID
    updated_at: datetime
    is_active: bool
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ScenarioResponse(BaseModel):
    """
    Response model for Scenario API.
    """

    id: UUID
    description: str

    model_config = ConfigDict(from_attributes=True)


class PaginatedScenarioResponse(PaginatedApiResponse[ScenarioResponse]):
    """
    Paginated response model for Scenario.
    """


# --- Request Body Models ---
class ScenarioCreateBody(BaseModel):
    """
    Request model for creating an financial scenario.
    """

    description: str = Field(..., min_length=3, max_length=100)
    scenario_type: ScenarioType = Field(...)
    is_locked: bool = False
    assumptions: str | None = Field(None, min_length=3, max_length=2000)


class ScenarioUpdateBody(BaseModel):
    """
    Request model for updating an Scenario.
    """

    description: str = Field(..., min_length=3, max_length=100)
    scenario_type: ScenarioType = Field(...)
    is_locked: bool = False
    assumptions: str | None = Field(None, min_length=3, max_length=2000)


# --- Router ---
router = APIRouter(
    prefix="/scenarios",
    tags=["Scenarios"],
    dependencies=[
        Depends(get_current_user),
    ],
)


# --- Endpoints ---
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_financial_scenario_create_or_update)],
)
def create_financial_scenario(
    request_body: ScenarioCreateBody,
    repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    actor: Annotated[User, Depends(get_current_user)],
):
    """
    Create a new financial scenario.
    """

    try:
        use_case = CreateScenarioUseCase(repo)

        input_dto = CreateScenarioInputDTO(
            actor=actor,
            description=request_body.description,
            scenario_type=request_body.scenario_type,
            is_locked=request_body.is_locked,
            assumptions=request_body.assumptions,
        )
        result = use_case.execute(input_dto)
        return {"id": result.id}
    except InvalidScenarioError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        ) from e


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedScenarioResponse,
    dependencies=[Depends(require_financial_scenario_read)],
)
def list_financial_scenarios(
    repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    actor: Annotated[User, Depends(get_current_user)],
    description: str | None = Query(None, description="Filter by description"),
    sort_by: str | None = Query("description", description="Sort field"),
    sort_order: str = Query("asc", enum=["asc", "desc"], description="Sort order"),
    offset: int = Query(0, ge=0, description="Offset"),
    limit: int = Query(10, ge=1, le=100, description="Limit"),
):
    """
    List financial_scenarios with filters, order and pagination.
    """

    filters = {}
    if description:
        filters["description"] = description

    input_dto = ListRequestInputDTO(
        actor=actor,
        filters=filters,
        sort_by=sort_by,
        sort_order=sort_order,
        offset=offset,
        limit=limit,
    )

    use_case = ListScenarioUseCase(repo)
    result = use_case.execute(input_dto)
    return result


@router.get(
    "/{financial_scenario_id}",
    status_code=status.HTTP_200_OK,
    response_model=ScenarioDetailResponse,
    dependencies=[Depends(require_financial_scenario_read)],
)
def get_financial_scenario_by_id(
    financial_scenario_id: UUID,
    repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    actor: Annotated[User, Depends(get_current_user)],
):
    """
    Get an financial scenario by its ID.
    """

    try:
        use_case = GetScenarioByIdUseCase(repo)
        input_dto = GetByIdRequestInputDTO(id=financial_scenario_id, actor=actor)
        financial_scenario = use_case.execute(input_dto)
        return financial_scenario
    except ScenarioNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        ) from e


@router.put(
    "/{financial_scenario_id}",
    status_code=status.HTTP_200_OK,
    response_model=ScenarioResponse,
    dependencies=[Depends(require_financial_scenario_create_or_update)],
)
def update_financial_scenario(
    financial_scenario_id: UUID,
    request_body: ScenarioUpdateBody,
    repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    actor: Annotated[User, Depends(get_current_user)],
):
    """
    Update an existing financial scenario.
    """

    try:
        use_case = UpdateScenarioUseCase(repo)

        input_dto = UpdateScenarioInputDTO(
            actor=actor,
            id=financial_scenario_id,
            description=request_body.description,
            scenario_type=request_body.scenario_type,
            is_locked=request_body.is_locked,
            assumptions=request_body.assumptions,
        )

        output_dto = use_case.execute(input_dto)

        return output_dto
    except ScenarioNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except InvalidScenarioError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        ) from e


@router.delete(
    "/{financial_scenario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_financial_scenario_delete)],
)
def delete_financial_scenario(
    financial_scenario_id: UUID,
    repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    actor: Annotated[User, Depends(get_current_user)],
):
    """
    Delete an existing financial scenario (soft delete).
    """

    try:
        use_case = DeleteScenarioUseCase(repo)
        use_case.execute(DeleteRequestInputDTO(id=financial_scenario_id, actor=actor))
    except ScenarioNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.patch(
    "/{financial_scenario_id}/restore",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_financial_scenario_delete)],
)
def restore_financial_scenario(
    financial_scenario_id: UUID,
    repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    actor: Annotated[User, Depends(get_current_user)],
):
    """
    Restore a soft-deleted financial scenario.
    """

    try:
        use_case = RestoreScenarioUseCase(repo)
        use_case.execute(RestoreRequestInputDTO(id=financial_scenario_id, actor=actor))
    except ScenarioNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.patch(
    "/{financial_scenario_id}/lock",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_financial_scenario_create_or_update)],
)
def lock_financial_scenario(
    financial_scenario_id: UUID,
    repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    actor: Annotated[User, Depends(get_current_user)],
):
    """
    Lock a financial scenario.
    """

    try:
        use_case = LockScenarioUseCase(repo)
        use_case.execute(LockScenarioInputDTO(id=financial_scenario_id, actor=actor))
    except ScenarioNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except ScenarioAlreadyLockedError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e


@router.patch(
    "/{financial_scenario_id}/unlock",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_financial_scenario_create_or_update)],
)
def unlock_financial_scenario(
    financial_scenario_id: UUID,
    repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    actor: Annotated[User, Depends(get_current_user)],
):
    """
    Unlock a financial scenario.
    """

    try:
        use_case = UnlockScenarioUseCase(repo)
        use_case.execute(UnlockScenarioInputDTO(id=financial_scenario_id, actor=actor))
    except ScenarioNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except ScenarioAlreadyUnlockedError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
