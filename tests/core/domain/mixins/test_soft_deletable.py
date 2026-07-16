from datetime import UTC, datetime

from src.core.domain.mixins.soft_deletable import SoftDeletableMixin


class TestSoftDeletableMixin:
    """
    Test suite for the SoftDeletableMixin.
    """

    def test_soft_delete(self):
        """
        Test that soft_delete correctly sets is_active to False and deleted_at to the current time.
        """

        class MyEntity(SoftDeletableMixin):
            pass

        entity = MyEntity()
        assert entity.is_active is True
        assert entity.deleted_at is None

        entity.soft_delete()

        assert entity.is_active is False
        assert isinstance(entity.deleted_at, datetime)
        # Check if it's close to now
        assert (datetime.now(UTC) - entity.deleted_at).total_seconds() < 1

    def test_restore(self):
        """
        Test that restore correctly sets is_active back to True and clears deleted_at.
        """

        class MyEntity(SoftDeletableMixin):
            pass

        entity = MyEntity()
        entity.soft_delete()
        assert entity.is_active is False
        assert entity.deleted_at is not None

        entity.restore()

        assert entity.is_active is True
        assert entity.deleted_at is None
