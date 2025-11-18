from decimal import Decimal

import pytest

from src.identity_access_management.application.use_cases.user import (
    InsufficientPermissionError,
)
from src.identity_access_management.domain.constants import AppPermission
from src.tenant_management.application.use_cases.tenant.queries import (
    ListTenantsInputDTO,
    ListTenantsUseCase,
)
from src.tenant_management.domain.entities import Plan, Tenant
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
def list_tenants_use_case(tenant_repo):
    """
    Fixture for ListTenantsUseCase.
    """

    return ListTenantsUseCase(tenant_repo)


class TestListTenantsUseCase:
    """
    Test suite for ListTenantsUseCase.
    """

    def test_user_with_permission_can_list_tenants(
        self,
        list_tenants_use_case,
        tenant_repo,
        admin_actor,
        plan_repo,
    ):
        """
        Test if a user with TENANT_READ permission can list tenants.
        """

        plans = plan_repo.search(tenant_id=None).data
        tenant1 = Tenant(
            name="Tenant A",
            created_by=admin_actor.id,
            plan_id=plans[0].id,
        )
        tenant2 = Tenant(
            name="Tenant B",
            created_by=admin_actor.id,
            plan_id=plans[0].id,
        )
        tenant_repo.save(tenant1)
        tenant_repo.save(tenant2)

        admin_actor.permissions.add(AppPermission.TENANT_READ)
        input_dto = ListTenantsInputDTO(actor=admin_actor)

        result = list_tenants_use_case.execute(input_dto)

        assert len(result) == 2
        assert tenant1 in result
        assert tenant2 in result

    def test_user_without_permission_cannot_list_tenants(
        self,
        list_tenants_use_case,
        admin_actor,
    ):
        """
        Test if a user without TENANT_READ permission cannot list tenants.
        """
        if AppPermission.TENANT_READ in admin_actor.permissions:
            admin_actor.permissions.remove(AppPermission.TENANT_READ)

        input_dto = ListTenantsInputDTO(actor=admin_actor)

        with pytest.raises(InsufficientPermissionError):
            list_tenants_use_case.execute(input_dto)

    def test_list_tenants_returns_empty_list_when_no_tenants_exist(
        self,
        list_tenants_use_case,
        admin_actor,
    ):
        """
        Test if list_tenants returns an empty list when no tenants exist.
        """

        admin_actor.permissions.add(AppPermission.TENANT_READ)
        input_dto = ListTenantsInputDTO(actor=admin_actor)
        result = list_tenants_use_case.execute(input_dto)
        assert result == []
