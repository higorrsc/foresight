from decimal import Decimal

import pytest

from src.identity_access_management.application.use_cases.user import (
    InsufficientPermissionError,
)
from src.identity_access_management.domain.constants import AppPermission
from src.tenant_management.application.use_cases.plan.queries import (
    ListPlansInputDTO,
    ListPlansUseCase,
)
from src.tenant_management.domain.entities import Plan
from tests.fakes import PlanInMemoryRepository


@pytest.fixture
def plan_repo():
    """
    Fixture for PlanInMemoryRepository.
    """

    return PlanInMemoryRepository()


@pytest.fixture
def list_plans_use_case(plan_repo):
    """
    Fixture for ListPlansUseCase.
    """

    return ListPlansUseCase(plan_repo)


class TestListPlansUseCase:
    """
    Test suite for ListPlansUseCase.
    """

    def test_user_with_permission_can_list_plans(
        self,
        list_plans_use_case,
        plan_repo,
        admin_actor,
    ):
        """
        Test if a user with PLAN_READ permission can list plans.
        """

        plan1 = Plan(name="Basic", price=Decimal("10.00"), created_by=admin_actor.id)
        plan2 = Plan(name="Premium", price=Decimal("20.00"), created_by=admin_actor.id)
        plan_repo.save(plan1)
        plan_repo.save(plan2)

        admin_actor.permissions.add(AppPermission.PLAN_READ)
        input_dto = ListPlansInputDTO(actor=admin_actor)

        result = list_plans_use_case.execute(input_dto)

        assert len(result.data) == 2
        assert plan1 in result.data
        assert plan2 in result.data

    def test_user_without_permission_cannot_list_plans(
        self,
        list_plans_use_case,
        admin_actor,
    ):
        """
        Test if a user without PLAN_READ permission cannot list plans.
        """

        if AppPermission.PLAN_READ in admin_actor.permissions:
            admin_actor.permissions.remove(AppPermission.PLAN_READ)

        input_dto = ListPlansInputDTO(actor=admin_actor)

        with pytest.raises(InsufficientPermissionError):
            list_plans_use_case.execute(input_dto)

    def test_list_plans_returns_empty_list_when_no_plans_exist(
        self,
        list_plans_use_case,
        admin_actor,
    ):
        """
        Test if list_plans returns an empty list when no plans exist.
        """

        admin_actor.permissions.add(AppPermission.PLAN_READ)
        input_dto = ListPlansInputDTO(actor=admin_actor)
        result = list_plans_use_case.execute(input_dto)
        assert result.data == []
