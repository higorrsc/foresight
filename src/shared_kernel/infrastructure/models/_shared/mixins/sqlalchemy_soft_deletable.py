from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy.orm import declarative_mixin, declared_attr


@declarative_mixin
class SQLAlchemySoftDeletableMixin:
    """
    Fields for soft delete in SQLAlchemy models.

    Include fields:
        - is_active (bool): Boolean that indicate if record is deleted
        - deleted_at (datetime): Timestamp when the record was deleted.
    """

    @declared_attr
    def is_active(cls):  # pylint: disable=E0213
        """
        Add is active field for soft delete.
        """

        return Column(
            Boolean,
            default=True,
            nullable=False,
            index=True,
        )

    @declared_attr
    def deleted_at(cls):  # pylint: disable=E0213
        """
        Add date of soft delete.
        """

        return Column(
            DateTime(timezone=True),
            nullable=True,
        )

    def soft_delete(self):
        """
        Soft delete the entity.
        """

        self.is_active = False
        self.deleted_at = datetime.now(timezone.utc)
