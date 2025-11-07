from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin, declared_attr

from src.shared_kernel.infrastructure.config import GUID_Type


@declarative_mixin
class SQLAlchemyBasicFields:
    """
    Basic fields for SQLAlchemy models.

    Include common audit and identification fields:
        - id (UUID): Primary key.
        - created_at (datetime): Timestamp when the record was created.
        - updated_at (datetime): Timestamp when the record was last updated.
    """

    @declared_attr
    def id(cls):  # pylint: disable=E0213
        """
        Add ID field.
        """

        return Column(
            GUID_Type,
            primary_key=True,
            default=uuid4,
        )

    @declared_attr
    def created_at(cls):  # pylint: disable=E0213
        """
        Add Timestamp when the record was created.
        """

        return Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
        )

    @declared_attr
    def updated_at(cls):  # pylint: disable=E0213
        """
        Add Timestamp when the record was updated.
        """

        return Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
        )
