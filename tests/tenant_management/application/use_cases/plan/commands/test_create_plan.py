from decimal import Decimal

import pytest

from src.identity_access_management.application.use_cases.permission import (
    InsufficientPermissionError,
)
from src.identity_access_management.domain.constants import AppPermission
from src.tenant_management.application.use_cases.plan.commands import (
    CreatePlanInputDTO,
    CreatePlanUseCase,
)
from tests.fakes import PlanInMemoryRepository


@pytest.fixture
def plan_repo():
    """
    Fixture for PlanInMemoryRepository.
    """

    return PlanInMemoryRepository()


@pytest.fixture
def create_plan_use_case(plan_repo):
    """
    Fixture for CreatePlanUseCase.
    """

    return CreatePlanUseCase(plan_repo)


class TestCreatePlanUseCase:
    """
    Test suite for CreatePlanUseCase.
    """

    def test_admin_can_create_plan(self, create_plan_use_case, plan_repo, admin_actor):
        """
        Test if admin can create a plan.
        """

        admin_actor.permissions.add(AppPermission.PLAN_CREATE)

        input_dto = CreatePlanInputDTO(
            actor=admin_actor,
            name="Pro Plan",
            price=Decimal(99.90),
        )

        result = create_plan_use_case.execute(input_dto)

        assert result.id is not None
        saved_plan = plan_repo.get_by_id(result.id, None)
        assert saved_plan.name == "Pro Plan"
        assert saved_plan.price == 99.90
        assert saved_plan.created_by == admin_actor.id

    def test_user_without_permission_cannot_create_plan(
        self,
        create_plan_use_case,
        admin_actor,
    ):
        """
        Test if user without permission cannot create a plan.
        """

        if AppPermission.PLAN_CREATE in admin_actor.permissions:
            admin_actor.permissions.remove(AppPermission.PLAN_CREATE)

        input_dto = CreatePlanInputDTO(actor=admin_actor, name="Hacker Plan")

        with pytest.raises(InsufficientPermissionError):
            create_plan_use_case.execute(input_dto)
