from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from src.api.dependencies import (
    PermissionChecker,
    get_current_user,
    get_plan_repository,
)
from src.api.routers._shared.dto import PaginatedApiResponse
from src.identity_access_management.application.use_cases.permission import (
    InsufficientPermissionError,
)
from src.identity_access_management.domain.entities import User
from src.tenant_management.application.use_cases.plan.commands import (
    CreatePlanInputDTO,
    CreatePlanUseCase,
)
from src.tenant_management.application.use_cases.plan.queries import (
    ListPlansInputDTO,
    ListPlansUseCase,
)
from src.tenant_management.domain.repositories import IPlanRepository

require_plan_create = PermissionChecker(["plan:create"])
require_plan_read = PermissionChecker(["plan:read"])


class PlanCreateBody(BaseModel):
    """
    Request model for API.
    """

    name: str = Field(..., min_length=3, max_length=50)
    price: float = Field(..., ge=0)


class PlanResponse(BaseModel):
    """
    Response model for API.
    """

    id: UUID
    name: str
    price: float

    model_config = ConfigDict(from_attributes=True)


class PaginatedPlanResponse(PaginatedApiResponse[PlanResponse]):
    """
    Paginated response model for Plans.
    """


router = APIRouter(prefix="/plans", tags=["Plans"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
    dependencies=[Depends(require_plan_create)],
)
def create_plan_endpoint(
    body: PlanCreateBody,
    repo: Annotated[IPlanRepository, Depends(get_plan_repository)],
    actor: Annotated[User, Depends(get_current_user)],
):
    """
    Create a new subscription plan (Super Admin only).
    """
    try:
        use_case = CreatePlanUseCase(repo)
        input_dto = CreatePlanInputDTO(
            actor=actor,
            name=body.name,
            price=Decimal(body.price),
        )
        result = use_case.execute(input_dto)
        return {"id": result.id}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        ) from e


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedPlanResponse,
    dependencies=[Depends(require_plan_read)],
)
def list_plans_endpoint(
    repo: Annotated[IPlanRepository, Depends(get_plan_repository)],
    actor: Annotated[User, Depends(get_current_user)],
):
    """
    List all available plans.
    """

    try:
        use_case = ListPlansUseCase(repo)
        input_dto = ListPlansInputDTO(actor=actor)
        plans = use_case.execute(input_dto)
        return plans
    except InsufficientPermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        ) from e
