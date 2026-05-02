from sqlalchemy.orm import Session

from src.core.infrastructure.db.seeding import seed_initial_data
from src.identity_access_management.infrastructure.models import (
    PermissionModel,
    RoleModel,
    UserModel,
)
from src.tenant_management.infrastructure.models import PlanModel, TenantModel


class TestSeeding:
    def test_seed_initial_data(self, db_session_for_test: Session):
        # The fixture already calls seed_initial_data,
        # but let's clear it and call it again to be sure,
        # OR just verify what's already there.
        # Given how db_session_for_test is defined, it's already seeded.

        # Verify Plan
        plan = db_session_for_test.query(PlanModel).filter_by(name="Standard").first()
        assert plan is not None
        from decimal import Decimal

        assert plan.price == Decimal("0.01")

        # Verify Tenant
        tenant = (
            db_session_for_test.query(TenantModel)
            .filter_by(name="System Tenant")
            .first()
        )
        assert tenant is not None
        assert tenant.plan_id == plan.id  # type: ignore

        # Verify Roles
        admin_role = (
            db_session_for_test.query(RoleModel)
            .filter_by(
                name="admin",
                tenant_id=tenant.id,
            )
            .first()
        )
        guest_role = (
            db_session_for_test.query(RoleModel)
            .filter_by(
                name="guest",
                tenant_id=tenant.id,
            )
            .first()
        )
        assert admin_role is not None
        assert guest_role is not None

        # Verify Permissions
        permissions = db_session_for_test.query(PermissionModel).all()
        assert len(permissions) > 0
        assert len(admin_role.permissions_rel) == len(permissions)

        # Verify Users
        admin_user = (
            db_session_for_test.query(UserModel)
            .filter_by(
                username="admin",
                tenant_id=tenant.id,
            )
            .first()
        )
        guest_user = (
            db_session_for_test.query(UserModel)
            .filter_by(
                username="guest",
                tenant_id=tenant.id,
            )
            .first()
        )
        assert admin_user is not None
        assert guest_user is not None
        assert admin_role in admin_user.roles_rel
        assert guest_role in guest_user.roles_rel

    def test_seeding_idempotency(self, db_session_for_test: Session):
        # Call seeding again
        seed_initial_data(db_session_for_test)

        # Verify counts haven't changed (assuming seed_initial_data is idempotent)
        assert db_session_for_test.query(PlanModel).count() == 1
        assert db_session_for_test.query(TenantModel).count() == 1
        assert db_session_for_test.query(RoleModel).count() == 2
        assert db_session_for_test.query(UserModel).count() == 2
