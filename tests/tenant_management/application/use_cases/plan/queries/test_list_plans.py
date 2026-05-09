from decimal import Decimal

import pytest

from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.exceptions import InsufficientPermissionError
from src.tenant_management.application.use_cases.plan.queries import (
    ListPlansInputDTO,
)
from src.tenant_management.domain.entities import Plan


class TestListPlansUseCase:
    """
    Test suite for ListPlansUseCase.
    """

    async def test_user_with_permission_can_list_plans(
        self,
        list_plans_use_case,
        plan_in_memory_repo,
        guest_actor,
    ):
        """
        Test if a user with PLAN_READ permission can list plans.
        """

        plan1 = Plan(name="Basic", price=Decimal("10.00"), created_by=guest_actor.id)
        plan2 = Plan(name="Premium", price=Decimal("20.00"), created_by=guest_actor.id)
        await plan_in_memory_repo.save(plan1)
        await plan_in_memory_repo.save(plan2)

        guest_actor.permissions.add(AppPermission.PLAN_READ)
        input_dto = ListPlansInputDTO(actor=guest_actor)

        result = await list_plans_use_case.execute(input_dto)

        assert len(result.data) == 2
        assert plan1 in result.data
        assert plan2 in result.data

    async def test_user_without_permission_cannot_list_plans(
        self,
        list_plans_use_case,
        guest_actor,
    ):
        """
        Test if a user without PLAN_READ permission cannot list plans.
        """

        if AppPermission.PLAN_READ in guest_actor.permissions:
            guest_actor.permissions.remove(AppPermission.PLAN_READ)

        input_dto = ListPlansInputDTO(actor=guest_actor)

        with pytest.raises(InsufficientPermissionError):
            await list_plans_use_case.execute(input_dto)

    async def test_list_plans_returns_empty_list_when_no_plans_exist(
        self,
        list_plans_use_case,
        guest_actor,
    ):
        """
        Test if list_plans returns an empty list when no plans exist.
        """

        guest_actor.permissions.add(AppPermission.PLAN_READ)
        input_dto = ListPlansInputDTO(actor=guest_actor)
        result = await list_plans_use_case.execute(input_dto)
        assert result.data == []
