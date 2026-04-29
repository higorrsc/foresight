from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy.orm import declarative_mixin, declared_attr, relationship

from .custom_types import GUID_Type


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


@declarative_mixin
class SQLAlchemyUserAuditFields:
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


@declarative_mixin
class SQLAlchemyTenantMixin:
    """
    Tenant mixin for SQLAlchemy models.
    """

    @declared_attr
    def tenant_id(cls):  # pylint: disable=E0213
        """
        Add TenantID field.
        """

        return Column(
            GUID_Type,
            ForeignKey("tenants.id"),
            nullable=False,
            index=True,
        )

    @declared_attr
    def tenant(cls):  # pylint: disable=E0213
        """
        Add TenantModel relationship.
        """

        return relationship(
            "TenantModel",
            foreign_keys=[cls.tenant_id],
            lazy="joined",
        )
