from decimal import Decimal

from src.identity_access_management.application.use_cases.user.commands import (
    OnboardingInputDTO,
)
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.entities import Permission
from src.tenant_management.domain.entities.plan import Plan


class TestOnboardingUseCase:
    """
    Test suite for the OnboardingUseCase.
    """

    async def test_onboarding_creates_all_entities_correctly(
        self,
        onboarding_use_case,
        plan_in_memory_repo,
        tenant_in_memory_repo,
        role_in_memory_repo,
        user_in_memory_repo,
        permission_in_memory_repo,
    ):
        """
        Test if the onboarding use case creates all entities correctly.
        """

        await plan_in_memory_repo.save(Plan(name="Standard", price=Decimal(1)))
        for perm_name in AppPermission.get_all_permissions():
            await permission_in_memory_repo.save(
                Permission(codename=perm_name, description="...")
            )

        input_dto = OnboardingInputDTO(
            tenant_name="Empresa Acme",
            username="admin_acme",
            password="password123",
            first_name="Admin",
            email="admin@acme.com",
        )

        output = await onboarding_use_case.execute(input_dto)

        assert output.tenant_id is not None
        assert output.user_id is not None

        tenant = await tenant_in_memory_repo.get_by_id(output.tenant_id, None)
        assert tenant is not None
        assert tenant.name == "Empresa Acme"

        user = await user_in_memory_repo.get_by_id(output.user_id, tenant.id)
        assert user is not None
        assert user.username == "admin_acme"
        assert user.tenant_id == tenant.id

        admin_role = await role_in_memory_repo.get_by_name("admin", tenant.id)
        guest_role = await role_in_memory_repo.get_by_name("guest", tenant.id)
        assert admin_role is not None
        assert guest_role is not None

        assert user.roles == {"admin"}

        assert len(admin_role.permissions) == len(AppPermission.get_all_permissions())
