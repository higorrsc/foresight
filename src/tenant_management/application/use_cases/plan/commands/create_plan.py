from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.exceptions import InsufficientPermissionError
from src.tenant_management.domain.entities import Plan
from src.tenant_management.domain.exceptions import InvalidPlanError
from src.tenant_management.domain.repositories import IPlanRepository

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class CreatePlanInputDTO:
    """
    Data Transfer Object for input data when creating a new plan.
    """

    actor: "User"
    name: str
    price: Decimal = Decimal(0)


@dataclass(frozen=True)
class CreatePlanOutputDTO:
    """
    Data Transfer Object for output data when creating a new plan.
    """

    id: UUID


class CreatePlanUseCase:
    """
    Use case for creating a new plan.
    """

    def __init__(self, repository: IPlanRepository):
        """
        Constructor for CreatePlanUseCase.
        """

        self._repository = repository

    def execute(self, input_dto: CreatePlanInputDTO) -> CreatePlanOutputDTO:
        """
        Execute the use case to create a new plan.
        """

        if AppPermission.PLAN_CREATE not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to create plans."
            )

        if self._repository.get_by_name(input_dto.name):
            raise InvalidPlanError(f"Plan with name '{input_dto.name}' already exists.")

        plan = Plan(
            name=input_dto.name,
            price=input_dto.price,
        )

        plan.created_by = input_dto.actor.id
        plan.updated_by = input_dto.actor.id

        self._repository.save(plan)
        return CreatePlanOutputDTO(id=plan.id)
