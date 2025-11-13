# tests/core/iam/application/use_cases/user/test_onboarding.py
from decimal import Decimal

import pytest

from src.identity_access_management.application.use_cases.user.commands import (
    OnboardingInputDTO,
    OnboardingUseCase,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities import Permission
from src.tenant_management.domain.entities.plan import Plan
from tests.fakes.in_memory_repository import (
    PermissionInMemoryRepository,
    PlanInMemoryRepository,
    RoleInMemoryRepository,
    TenantInMemoryRepository,
    UserInMemoryRepository,
)


@pytest.fixture
def user_repo():
    """
    Fixture that represents a user repository.
    """

    return UserInMemoryRepository()


@pytest.fixture
def role_repo():
    """
    Fixture that represents a role repository.
    """

    return RoleInMemoryRepository()


@pytest.fixture
def perm_repo():
    """
    Fixture that represents a permission repository.
    """

    return PermissionInMemoryRepository()


@pytest.fixture
def tenant_repo():
    """
    Fixture that represents a tenant repository.
    """

    return TenantInMemoryRepository()


@pytest.fixture
def plan_repo():
    """
    Fixture that represents a plan repository.
    """

    return PlanInMemoryRepository()


@pytest.fixture
def onboarding_use_case(
    plan_repo,
    tenant_repo,
    role_repo,
    user_repo,
    perm_repo,
):
    return OnboardingUseCase(
        plan_repository=plan_repo,
        tenant_repository=tenant_repo,
        role_repository=role_repo,
        user_repository=user_repo,
        permission_repository=perm_repo,
    )


class TestOnboardingUseCase:
    """
    Test suite for the OnboardingUseCase.
    """

    def test_onboarding_creates_all_entities_correctly(
        self,
        onboarding_use_case,
        plan_repo,
        tenant_repo,
        role_repo,
        user_repo,
        perm_repo,
    ):
        """
        Test if the onboarding use case creates all entities correctly.
        """

        plan_repo.save(Plan(name="Standard", price=Decimal(1)))
        for perm_name in AppPermission.get_all_permissions():
            perm_repo.save(Permission(codename=perm_name, description="..."))

        input_dto = OnboardingInputDTO(
            tenant_name="Empresa Acme",
            username="admin_acme",
            password="password123",
            first_name="Admin",
            email="admin@acme.com",
        )

        output = onboarding_use_case.execute(input_dto)

        assert output.tenant_id is not None
        assert output.user_id is not None

        tenant = tenant_repo.get_by_id(output.tenant_id, None)
        assert tenant is not None
        assert tenant.name == "Empresa Acme"

        user = user_repo.get_by_id(output.user_id, tenant.id)
        assert user is not None
        assert user.username == "admin_acme"
        assert user.tenant_id == tenant.id

        admin_role = role_repo.get_by_name("admin", tenant.id)
        guest_role = role_repo.get_by_name("guest", tenant.id)
        assert admin_role is not None
        assert guest_role is not None

        assert user.roles == {"admin"}

        assert len(admin_role.permissions) == len(AppPermission.get_all_permissions())
