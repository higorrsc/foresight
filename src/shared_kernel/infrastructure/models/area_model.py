from sqlalchemy import Column, String

from src.core.infrastructure.config import SQLAlchemyBase
from src.core.infrastructure.config.mixins import (
    SQLAlchemySoftDeletableMixin,
    SQLAlchemyTenantMixin,
    SQLAlchemyUserAuditMixin,
)


class AreaModel(
    SQLAlchemyBase,
    SQLAlchemySoftDeletableMixin,
    SQLAlchemyTenantMixin,
    SQLAlchemyUserAuditMixin,
):
    """
    SQLAlchemy model for the Area entity.
    """

    __tablename__ = "areas"

    description = Column(
        String(100),
        nullable=False,
    )
