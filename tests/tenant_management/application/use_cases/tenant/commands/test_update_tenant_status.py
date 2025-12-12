from decimal import Decimal
from uuid import uuid4

import pytest

from src.identity_access_management.application.use_cases.permission import (
    InsufficientPermissionError,
)
from src.identity_access_management.domain.constants import AppPermission
from src.tenant_management.application.use_cases.tenant import TenantNotFoundError
from src.tenant_management.application.use_cases.tenant.commands import (
    UpdateTenantStatusInputDTO,
    UpdateTenantStatusUseCase,
)
from src.tenant_management.domain.entities import Tenant
from src.tenant_management.domain.entities.plan import Plan
from src.tenant_management.domain.value_objects import TenantStatus
from tests.fakes import PlanInMemoryRepository, TenantInMemoryRepository


@pytest.fixture
def plan_repo():
    """
    Fixture for PlanInMemoryRepository.
    """

    return PlanInMemoryRepository(
        [
            Plan(
                name="Pro Plan",
                price=Decimal(99.90),
            ),
            Plan(
                name="Light Plan",
                price=Decimal(9.90),
            ),
            Plan(
                name="Free Plan",
                price=Decimal(0.01),
            ),
        ]
    )


@pytest.fixture
def tenant_repo():
    """
    Fixture for TenantInMemoryRepository.
    """

    return TenantInMemoryRepository()


@pytest.fixture
def update_tenant_status_use_case(tenant_repo):
    """
    Fixture for UpdateTenantStatusUseCase.
    """

    return UpdateTenantStatusUseCase(tenant_repo)


class TestUpdateTenantStatusUseCase:
    """
    Test suite for UpdateTenantStatusUseCase.
    """

    def test_user_with_permission_can_update_tenant_status(
        self,
        update_tenant_status_use_case,
        tenant_repo,
        admin_actor,
        plan_repo,
    ):
        """
        Test if a user with TENANT_UPDATE permission can update a tenant's status.
        """

        plans = plan_repo.search(tenant_id=None).data
        tenant = Tenant(
            name="Test Tenant",
            created_by=admin_actor.id,
            plan_id=plans[0].id,
        )
        tenant_repo.save(tenant)

        admin_actor.permissions.add(AppPermission.TENANT_UPDATE)
        input_dto = UpdateTenantStatusInputDTO(
            actor=admin_actor,
            tenant_id_to_update=tenant.id,
            new_status=TenantStatus.INACTIVE,
        )

        update_tenant_status_use_case.execute(input_dto)

        updated_tenant = tenant_repo.get_by_id_global(tenant.id)
        assert updated_tenant is not None
        assert updated_tenant.status == TenantStatus.INACTIVE
        assert updated_tenant.updated_by == admin_actor.id

    def test_user_without_permission_cannot_update_tenant_status(
        self,
        update_tenant_status_use_case,
        admin_actor,
    ):
        """
        Test if a user without TENANT_UPDATE permission cannot update a tenant's status.
        """
        if AppPermission.TENANT_UPDATE in admin_actor.permissions:
            admin_actor.permissions.remove(AppPermission.TENANT_UPDATE)

        input_dto = UpdateTenantStatusInputDTO(
            actor=admin_actor,
            tenant_id_to_update=uuid4(),
            new_status=TenantStatus.INACTIVE,
        )

        with pytest.raises(InsufficientPermissionError):
            update_tenant_status_use_case.execute(input_dto)

    def test_updating_non_existent_tenant_raises_error(
        self,
        update_tenant_status_use_case,
        admin_actor,
    ):
        """
        Test that attempting to update a non-existent tenant raises TenantNotFoundError.
        """
        non_existent_tenant_id = uuid4()
        admin_actor.permissions.add(AppPermission.TENANT_UPDATE)

        input_dto = UpdateTenantStatusInputDTO(
            actor=admin_actor,
            tenant_id_to_update=non_existent_tenant_id,
            new_status=TenantStatus.INACTIVE,
        )

        with pytest.raises(TenantNotFoundError):
            update_tenant_status_use_case.execute(input_dto)
