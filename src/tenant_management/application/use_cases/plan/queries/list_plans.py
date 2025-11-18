from dataclasses import dataclass
from typing import TYPE_CHECKING, List

from src.identity_access_management.application.use_cases.user import (
    InsufficientPermissionError,
)
from src.identity_access_management.domain.constants import AppPermission
from src.tenant_management.domain.entities import Plan
from src.tenant_management.domain.repositories import IPlanRepository

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class ListPlansInputDTO:
    """
    Data Transfer Object for input data when listing plans.
    """

    actor: "User"


class ListPlansUseCase:
    """
    Use case for listing plans.
    """

    def __init__(self, repository: IPlanRepository):
        """
        Constructor for ListPlansUseCase.
        """

        self._repository = repository

    def execute(self, input_dto: ListPlansInputDTO) -> List[Plan]:
        """
        Execute the use case to list plans.
        """

        if AppPermission.PLAN_READ not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to list plans."
            )

        return self._repository.search(tenant_id=None).data
