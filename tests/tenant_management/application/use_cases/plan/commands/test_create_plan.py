from decimal import Decimal

import pytest

from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.exceptions import InsufficientPermissionError
from src.tenant_management.application.use_cases.plan.commands import (
    CreatePlanInputDTO,
)


class TestCreatePlanUseCase:
    """
    Test suite for CreatePlanUseCase.
    """

    async def test_admin_can_create_plan(
        self, create_plan_use_case, plan_in_memory_repo, guest_actor
    ):
        """
        Test if admin can create a plan.
        """

        guest_actor.permissions.add(AppPermission.PLAN_CREATE)

        input_dto = CreatePlanInputDTO(
            actor=guest_actor,
            name="Pro Plan",
            price=Decimal(99.90),
        )

        result = await create_plan_use_case.execute(input_dto)

        assert result.id is not None
        saved_plan = await plan_in_memory_repo.get_by_id(result.id, None)
        assert saved_plan.name == "Pro Plan"
        assert saved_plan.price == 99.90
        assert saved_plan.created_by == guest_actor.id

    async def test_user_without_permission_cannot_create_plan(
        self,
        create_plan_use_case,
        guest_actor,
    ):
        """
        Test if user without permission cannot create a plan.
        """

        if AppPermission.PLAN_CREATE in guest_actor.permissions:
            guest_actor.permissions.remove(AppPermission.PLAN_CREATE)

        input_dto = CreatePlanInputDTO(actor=guest_actor, name="Hacker Plan")

        with pytest.raises(InsufficientPermissionError):
            await create_plan_use_case.execute(input_dto)
