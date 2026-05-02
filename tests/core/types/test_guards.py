from uuid import uuid4

from src.core.types.guards import has_tenant, is_soft_deletable, is_user_auditable


class TestGuards:
    def test_has_tenant(self):
        class TenantObj:
            tenant_id = uuid4()

        class NoTenantObj:
            pass

        assert has_tenant(TenantObj()) is True
        assert has_tenant(NoTenantObj()) is False
        assert has_tenant({}) is False

    def test_is_soft_deletable(self):
        class SoftDeletableObj:
            is_active = True

        class NotSoftDeletableObj:
            pass

        assert is_soft_deletable(SoftDeletableObj()) is True
        assert is_soft_deletable(NotSoftDeletableObj()) is False
        assert is_soft_deletable({}) is False

    def test_is_user_auditable(self):
        class UserAuditableObj:
            created_by = uuid4()
            updated_by = uuid4()

        class NotUserAuditableObj:
            created_by = uuid4()

        class AnotherNotUserAuditableObj:
            updated_by = uuid4()

        assert is_user_auditable(UserAuditableObj()) is True
        assert is_user_auditable(NotUserAuditableObj()) is False
        assert is_user_auditable(AnotherNotUserAuditableObj()) is False
        assert is_user_auditable({}) is False
