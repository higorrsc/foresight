from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.identity_access_management.infrastructure.models import (
    PermissionModel,
    RoleModel,
    UserModel,
)
from src.scripts.seed import seed_initial_data
from src.tenant_management.infrastructure.models import PlanModel, TenantModel


class TestSeed:
    """
    Test suite for the database seeding process.
    """

    async def test_seed_initial_data(self, db_session_for_test: AsyncSession):
        """
        Test that seed_initial_data correctly populates the database with initial records.
        """
        # The fixture already calls seed_initial_data,
        # but let's clear it and call it again to be sure,
        # OR just verify what's already there.
        # Given how db_session_for_test is defined, it's already seeded.

        # Verify Plan
        stmt_plan = select(PlanModel).where(PlanModel.name == "Standard")
        result_plan = await db_session_for_test.execute(stmt_plan)
        plan = result_plan.unique().scalar_one_or_none()

        assert plan is not None
        from decimal import Decimal

        assert plan.price == Decimal("0.01")

        # Verify Tenant
        stmt_tenant = select(TenantModel).where(TenantModel.name == "System Tenant")
        result_tenant = await db_session_for_test.execute(stmt_tenant)
        tenant = result_tenant.unique().scalar_one_or_none()

        assert tenant is not None
        assert tenant.plan_id == plan.id  # type: ignore

        # Verify Roles
        stmt_admin_role = (
            select(RoleModel)
            .options(selectinload(RoleModel.permissions_rel))
            .where(RoleModel.name == "admin", RoleModel.tenant_id == tenant.id)
        )
        result_admin_role = await db_session_for_test.execute(stmt_admin_role)
        admin_role = result_admin_role.unique().scalar_one_or_none()

        stmt_guest_role = select(RoleModel).where(
            RoleModel.name == "guest", RoleModel.tenant_id == tenant.id
        )
        result_guest_role = await db_session_for_test.execute(stmt_guest_role)
        guest_role = result_guest_role.unique().scalar_one_or_none()

        assert admin_role is not None
        assert guest_role is not None

        # Verify Permissions
        stmt_permissions = select(PermissionModel)
        result_permissions = await db_session_for_test.execute(stmt_permissions)
        permissions = result_permissions.unique().scalars().all()

        assert len(permissions) > 0
        assert len(admin_role.permissions_rel) == len(permissions)

        # Verify Users
        stmt_admin_user = (
            select(UserModel)
            .options(selectinload(UserModel.roles_rel))
            .where(UserModel.username == "admin", UserModel.tenant_id == tenant.id)
        )
        result_admin_user = await db_session_for_test.execute(stmt_admin_user)
        admin_user = result_admin_user.unique().scalar_one_or_none()

        stmt_guest_user = (
            select(UserModel)
            .options(selectinload(UserModel.roles_rel))
            .where(UserModel.username == "guest", UserModel.tenant_id == tenant.id)
        )
        result_guest_user = await db_session_for_test.execute(stmt_guest_user)
        guest_user = result_guest_user.unique().scalar_one_or_none()

        assert admin_user is not None
        assert guest_user is not None
        assert admin_role in admin_user.roles_rel
        assert guest_role in guest_user.roles_rel

    async def test_seeding_idempotency(self, db_session_for_test: AsyncSession):
        """
        Test that multiple calls to seed_initial_data do not create duplicate records.
        """

        # Call seeding again (it's an async function now)
        await seed_initial_data(db_session_for_test)

        # Verify counts haven't changed
        stmt_plan_count = select(func.count()).select_from(PlanModel)
        assert (await db_session_for_test.execute(stmt_plan_count)).scalar_one() == 1

        stmt_tenant_count = select(func.count()).select_from(TenantModel)
        assert (await db_session_for_test.execute(stmt_tenant_count)).scalar_one() == 1

        stmt_role_count = select(func.count()).select_from(RoleModel)
        assert (await db_session_for_test.execute(stmt_role_count)).scalar_one() == 2

        stmt_user_count = select(func.count()).select_from(UserModel)
        assert (await db_session_for_test.execute(stmt_user_count)).scalar_one() == 2
