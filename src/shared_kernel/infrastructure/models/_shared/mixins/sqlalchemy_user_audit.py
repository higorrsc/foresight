from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import declarative_mixin, declared_attr, relationship

from src.shared_kernel.infrastructure.config import GUID_Type


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
    def creator(cls):  # pylint: disable=E0213
        """
        Add UserModel relationship.
        """

        return relationship(
            "UserModel",
            foreign_keys=f"{cls.__name__}.created_by",
            lazy="joined",
        )

    @declared_attr
    def updater(cls):  # pylint: disable=E0213
        """
        Add UserModel relationship.
        """

        return relationship(
            "UserModel",
            foreign_keys=f"{cls.__name__}.updated_by",
            lazy="joined",
        )
