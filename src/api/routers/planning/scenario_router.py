from datetime import date, datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.api.dependencies import (
    PermissionChecker,
    get_current_user,
    get_exchange_rate_repository,
    get_scenario_repository,
)
from src.api.routers._shared import PaginatedApiResponse
from src.core.application.use_cases.commands import (
    DeleteRequestInputDTO,
    RestoreRequestInputDTO,
)
from src.core.application.use_cases.queries import (
    GetByIdRequestInputDTO,
    ListRequestInputDTO,
)
from src.identity_access_management.domain.entities import User
from src.planning.application.use_cases.scenario.commands import (
    AddExchangeRateInputDTO,
    AddExchangeRateToScenarioUseCase,
    CreateScenarioInputDTO,
    CreateScenarioUseCase,
    DeleteScenarioUseCase,
    ExchangeRateEntryDTO,
    LockScenarioInputDTO,
    LockScenarioUseCase,
    RemoveExchangeRateInputDTO,
    RemoveExchangeRateUseCase,
    RestoreScenarioUseCase,
    UnlockScenarioInputDTO,
    UnlockScenarioUseCase,
    UpdateExchangeRateInputDTO,
    UpdateExchangeRateUseCase,
    UpdateScenarioInputDTO,
    UpdateScenarioUseCase,
)
from src.planning.application.use_cases.scenario.queries import (
    GetScenarioByIdUseCase,
    GetScenarioDetailsUseCase,
    ListScenarioUseCase,
)
from src.planning.domain.entities.scenario import ScenarioType
from src.planning.domain.exceptions import (
    CannotUpdateLockedScenarioError,
    ExchangeRateNotFoundError,
    InvalidExchangeRateError,
    InvalidScenarioError,
    ScenarioAlreadyLockedError,
    ScenarioAlreadyUnlockedError,
    ScenarioNotFoundError,
)
from src.planning.domain.repositories import (
    IExchangeRateRepository,
    IScenarioRepository,
)

# --- Permissions ---
require_scenario_create_or_update = PermissionChecker(
    [
        "scenario:create",
        "scenario:update",
    ]
)
require_scenario_delete = PermissionChecker(
    [
        "scenario:delete",
    ]
)
require_scenario_read = PermissionChecker(
    [
        "scenario:read",
    ]
)


# --- Response Models ---
class ExchangeRateResponse(BaseModel):
    """
    Response model for Exchange Rate API.
    """

    id: UUID
    from_currency: str
    to_currency: str
    rate: Decimal
    effective_date: date

    # A MÁGICA ACONTECE AQUI:
    @field_validator("from_currency", "to_currency", mode="before")
    @classmethod
    def extract_currency_code(cls, v):
        """Extract the currency code from the value."""

        if hasattr(v, "value"):
            return str(v.value)

        return str(v)

    model_config = ConfigDict(from_attributes=True)


class ScenarioDetailResponse(BaseModel):
    """
    Response model for Scenario API (Detailed).
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
    exchange_rates: list[ExchangeRateResponse] | None = None

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
class ExchangeRateEntrySchema(BaseModel):
    """Individual rate item"""

    effective_date: date
    rate: Decimal = Field(gt=0)


class ExchangeRateCreateBody(BaseModel):
    """Request model for creating an exchange rate."""

    from_currency: str = Field(min_length=3, max_length=3)
    to_currency: str = Field(min_length=3, max_length=3)
    exchange: list[ExchangeRateEntrySchema] = Field(min_length=1)


class ScenarioCreateBody(BaseModel):
    """
    Request model for creating an financial scenario.
    """

    description: str = Field(min_length=3, max_length=100)
    scenario_type: ScenarioType
    is_locked: bool = False
    assumptions: str | None = Field(None, min_length=3, max_length=2000)


class ScenarioUpdateBody(BaseModel):
    """
    Request model for updating an Scenario.
    """

    description: str = Field(min_length=3, max_length=100)
    scenario_type: ScenarioType
    is_locked: bool = False
    assumptions: str | None = Field(None, min_length=3, max_length=2000)


class ExchangeRateUpdateBody(BaseModel):
    """
    Request model for updating an exchange rate.
    """

    rate: Decimal = Field(gt=0)


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
    dependencies=[Depends(require_scenario_create_or_update)],
)
async def create_financial_scenario(
    request_body: ScenarioCreateBody,
    repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> dict[str, UUID]:
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
        result = await use_case.execute(input_dto)
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
    dependencies=[Depends(require_scenario_read)],
)
async def list_financial_scenarios(
    repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    actor: Annotated[User, Depends(get_current_user)],
    description: Annotated[str | None, Query(description="Filter by description")] = None,
    sort_by: Annotated[str | None, Query(description="Sort field")] = "description",
    sort_order: Annotated[str, Query(enum=["asc", "desc"], description="Sort order")] = "asc",
    offset: Annotated[int, Query(ge=0, description="Offset")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Limit")] = 10,
) -> PaginatedScenarioResponse:
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
    result = await use_case.execute(input_dto)
    return result


@router.get(
    "/{scenario_id}",
    status_code=status.HTTP_200_OK,
    response_model=ScenarioResponse,
    dependencies=[Depends(require_scenario_read)],
)
async def get_scenario_by_id(
    scenario_id: Annotated[UUID, Path(description="The scenario ID")],
    repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> ScenarioResponse:
    """
    Get an financial scenario by its ID.
    """

    try:
        use_case = GetScenarioByIdUseCase(repo)
        input_dto = GetByIdRequestInputDTO(id=scenario_id, actor=actor)
        financial_scenario = await use_case.execute(input_dto)
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


@router.get(
    "/{scenario_id}/details",
    status_code=status.HTTP_200_OK,
    response_model=ScenarioDetailResponse,
    dependencies=[Depends(require_scenario_read)],
)
async def get_scenario_details(
    scenario_id: Annotated[UUID, Path(description="The scenario ID")],
    repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> ScenarioDetailResponse:
    """
    Get detailed information about a financial scenario.
    """

    try:
        use_case = GetScenarioDetailsUseCase(repo)
        input_dto = GetByIdRequestInputDTO(id=scenario_id, actor=actor)
        financial_scenario = await use_case.execute(input_dto)
        return financial_scenario
    except ScenarioNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.put(
    "/{scenario_id}",
    status_code=status.HTTP_200_OK,
    response_model=ScenarioResponse,
    dependencies=[Depends(require_scenario_create_or_update)],
)
async def update_financial_scenario(
    scenario_id: Annotated[UUID, Path(description="The scenario ID")],
    request_body: ScenarioUpdateBody,
    repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> ScenarioResponse:
    """
    Update an existing financial scenario.
    """

    try:
        use_case = UpdateScenarioUseCase(repo)

        input_dto = UpdateScenarioInputDTO(
            actor=actor,
            id=scenario_id,
            description=request_body.description,
            scenario_type=request_body.scenario_type,
            is_locked=request_body.is_locked,
            assumptions=request_body.assumptions,
        )

        output_dto = await use_case.execute(input_dto)

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
    "/{scenario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_scenario_delete)],
)
async def delete_financial_scenario(
    scenario_id: Annotated[UUID, Path(description="The scenario ID")],
    repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> None:
    """
    Delete an existing financial scenario (soft delete).
    """

    try:
        use_case = DeleteScenarioUseCase(repo)
        await use_case.execute(DeleteRequestInputDTO(id=scenario_id, actor=actor))
    except ScenarioNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.patch(
    "/{scenario_id}/restore",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_scenario_delete)],
)
async def restore_financial_scenario(
    scenario_id: Annotated[UUID, Path(description="The scenario ID")],
    repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> None:
    """
    Restore a soft-deleted financial scenario.
    """

    try:
        use_case = RestoreScenarioUseCase(repo)
        await use_case.execute(RestoreRequestInputDTO(id=scenario_id, actor=actor))
    except ScenarioNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.patch(
    "/{scenario_id}/lock",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_scenario_create_or_update)],
)
async def lock_financial_scenario(
    scenario_id: Annotated[UUID, Path(description="The scenario ID")],
    repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> None:
    """
    Lock a financial scenario.
    """

    try:
        use_case = LockScenarioUseCase(repo)
        await use_case.execute(LockScenarioInputDTO(id=scenario_id, actor=actor))
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
    "/{scenario_id}/unlock",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_scenario_create_or_update)],
)
async def unlock_financial_scenario(
    scenario_id: Annotated[UUID, Path(description="The scenario ID")],
    repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> None:
    """
    Unlock a financial scenario.
    """

    try:
        use_case = UnlockScenarioUseCase(repo)
        await use_case.execute(UnlockScenarioInputDTO(id=scenario_id, actor=actor))
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


# --- Exchange Rate Endpoints ---
@router.post(
    "/{scenario_id}/exchange-rates",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_scenario_create_or_update)],
)
async def add_exchange_rate_to_scenario(
    scenario_id: Annotated[UUID, Path(description="The scenario ID")],
    request_body: ExchangeRateCreateBody,
    scenario_repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> dict[str, UUID | int | str]:
    """
    Add a new exchange rate to a financial scenario.
    """

    try:
        use_case = AddExchangeRateToScenarioUseCase(scenario_repo)

        exchange_entries = [
            ExchangeRateEntryDTO(
                effective_date=entry.effective_date,
                rate=entry.rate,
            )
            for entry in request_body.exchange
        ]

        input_dto = AddExchangeRateInputDTO(
            actor=actor,
            scenario_id=scenario_id,
            from_currency=request_body.from_currency,
            to_currency=request_body.to_currency,
            exchange=exchange_entries,
        )
        result = await use_case.execute(input_dto)
        return {
            "scenario_id": result.scenario_id,
            "inserted_count": result.inserted_count,
            "message": "Exchange rate added successfully",
        }
    except ScenarioNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except CannotUpdateLockedScenarioError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
    except InvalidExchangeRateError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        ) from e


@router.put(
    "/exchange-rates/{exchange_rate_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_scenario_create_or_update)],
)
async def update_exchange_rate(
    exchange_rate_id: Annotated[UUID, Path(description="The exchange rate ID")],
    request_body: ExchangeRateUpdateBody,
    scenario_repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    exchange_rate_repo: Annotated[
        IExchangeRateRepository, Depends(get_exchange_rate_repository)
    ],
    actor: Annotated[User, Depends(get_current_user)],
) -> dict[str, str]:
    """
    Update an existing exchange rate.
    """

    try:
        use_case = UpdateExchangeRateUseCase(scenario_repo, exchange_rate_repo)
        input_dto = UpdateExchangeRateInputDTO(
            actor=actor,
            id=exchange_rate_id,
            rate=request_body.rate,
        )
        await use_case.execute(input_dto)
        return {"message": "Exchange rate updated successfully"}
    except ExchangeRateNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except ScenarioNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except CannotUpdateLockedScenarioError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
    except InvalidExchangeRateError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        ) from e


@router.delete(
    "/exchange-rates/{exchange_rate_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_scenario_create_or_update)],
)
async def remove_exchange_rate(
    exchange_rate_id: Annotated[UUID, Path(description="The exchange rate ID")],
    scenario_repo: Annotated[IScenarioRepository, Depends(get_scenario_repository)],
    exchange_rate_repo: Annotated[
        IExchangeRateRepository, Depends(get_exchange_rate_repository)
    ],
    actor: Annotated[User, Depends(get_current_user)],
) -> None:
    """
    Remove an exchange rate from a scenario.
    """

    try:
        use_case = RemoveExchangeRateUseCase(scenario_repo, exchange_rate_repo)
        input_dto = RemoveExchangeRateInputDTO(
            actor=actor,
            id=exchange_rate_id,
        )
        await use_case.execute(input_dto)
    except ExchangeRateNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except ScenarioNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except CannotUpdateLockedScenarioError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
