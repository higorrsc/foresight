from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import declarative_mixin, declared_attr, relationship

from src.core.infrastructure.config import GUIDType


@declarative_mixin
class SQLAlchemyUserAuditMixin:
    """
    User Audit fields for SQLAlchemy models.
    """

    @declared_attr
    def created_by(cls):  # noqa: N805
        """
        Add UserID that created the record.
        """

        return Column(
            GUIDType,
            ForeignKey(
                "users.id",
                ondelete="SET NULL",
            ),
            nullable=True,
        )

    @declared_attr
    def created_at(cls):  # noqa: N805
        """
        Add date of creation.
        """

        return Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(UTC),
        )

    @declared_attr
    def updated_by(cls):  # noqa: N805
        """
        Add UserID that updated the record.
        """

        return Column(
            GUIDType,
            ForeignKey(
                "users.id",
                ondelete="SET NULL",
            ),
            nullable=True,
        )

    @declared_attr
    def updated_at(cls):  # noqa: N805
        """
        Add date of update.
        """

        return Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(UTC),
            onupdate=lambda: datetime.now(UTC),
        )

    @declared_attr
    def creator(cls):  # noqa: N805
        """
        Add UserModel relationship.
        """

        return relationship(
            "UserModel",
            foreign_keys=f"{cls.__name__}.created_by",  # type: ignore
            lazy="joined",
        )

    @declared_attr
    def updater(cls):  # noqa: N805
        """
        Add UserModel relationship.
        """

        return relationship(
            "UserModel",
            foreign_keys=f"{cls.__name__}.updated_by",  # type: ignore
            lazy="joined",
        )
