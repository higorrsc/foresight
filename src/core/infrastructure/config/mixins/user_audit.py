from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import declarative_mixin, declared_attr, relationship

from src.core.infrastructure.config import GUID_Type


@declarative_mixin
class SQLAlchemyUserAuditMixin:
    """
    User Audit fields for SQLAlchemy models.
    """

    @declared_attr
    def created_by(cls):  # pylint: disable=E0213
        """
        Add UserID that created the record.
        """

        return Column(
            GUID_Type,
            ForeignKey(
                "users.id",
                ondelete="SET NULL",
            ),
            nullable=True,
        )

    @declared_attr
    def created_at(cls):  # pylint: disable=E0213
        """
        Add date of creation.
        """

        return Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
        )

    @declared_attr
    def updated_by(cls):  # pylint: disable=E0213
        """
        Add UserID that updated the record.
        """

        return Column(
            GUID_Type,
            ForeignKey(
                "users.id",
                ondelete="SET NULL",
            ),
            nullable=True,
        )

    @declared_attr
    def updated_at(cls):  # pylint: disable=E0213
        """
        Add date of update.
        """

        return Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
        )

    @declared_attr
    def creator(cls):  # pylint: disable=E0213
        """
        Add UserModel relationship.
        """

        return relationship(
            "UserModel",
            foreign_keys=f"{cls.__name__}.created_by",  # type: ignore
            lazy="joined",
        )

    @declared_attr
    def updater(cls):  # pylint: disable=E0213
        """
        Add UserModel relationship.
        """

        return relationship(
            "UserModel",
            foreign_keys=f"{cls.__name__}.updated_by",  # type: ignore
            lazy="joined",
        )
