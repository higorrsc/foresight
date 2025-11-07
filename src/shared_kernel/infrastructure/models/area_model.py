from sqlalchemy import Column, String

from src.shared_kernel.infrastructure.config.sqlalchemy_base import SQLAlchemyBase
from src.shared_kernel.infrastructure.models._shared.mixins import (
    SQLAlchemySoftDeletableMixin,
    SQLAlchemyTenantMixin,
)


class AreaModel(SQLAlchemyBase, SQLAlchemySoftDeletableMixin, SQLAlchemyTenantMixin):
    """
    SQLAlchemy model for the Area entity.
    """

    __tablename__ = "areas"

    description = Column(
        String(100),
        nullable=False,
    )
