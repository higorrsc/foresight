from datetime import UTC, datetime
from uuid import uuid4

from src.core.domain.mixins.user_audit import UserAuditMixin


class TestUserAuditMixin:
    """
    Test suite for the UserAuditMixin.
    """

    def test_update_audit_info(self):
        """
        Test that update_audit_info correctly updates updated_by and updated_at.
        """

        class MyEntity(UserAuditMixin):
            pass

        entity = MyEntity()
        user_id = uuid4()

        # Initial state (set by default_factory)
        assert entity.updated_by is None
        assert isinstance(entity.updated_at, datetime)

        # Capture initial updated_at
        initial_updated_at = entity.updated_at

        entity.update_audit_info(user_id)

        assert entity.updated_by == user_id
        assert entity.updated_at > initial_updated_at
        assert (datetime.now(UTC) - entity.updated_at).total_seconds() < 1

    def test_initial_state(self):
        """
        Test the initial state of an entity with UserAuditMixin.
        """

        class MyEntity(UserAuditMixin):
            pass

        entity = MyEntity()
        assert entity.created_by is None
        assert entity.updated_by is None
        assert isinstance(entity.created_at, datetime)
        assert isinstance(entity.updated_at, datetime)
