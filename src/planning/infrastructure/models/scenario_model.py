from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from src.core.infrastructure.config import SQLAlchemyBase
from src.core.infrastructure.config.mixins import (
    SQLAlchemySoftDeletableMixin,
    SQLAlchemyTenantMixin,
    SQLAlchemyUserAuditMixin,
)


class ScenarioModel(
    SQLAlchemyBase,
    SQLAlchemySoftDeletableMixin,
    SQLAlchemyTenantMixin,
    SQLAlchemyUserAuditMixin,
):
    """
    SQLAlchemy model for the Scenario entity.
    """

    __tablename__ = "scenarios"

    description = Column(
        String(100),
        nullable=False,
    )

    scenario_type = Column(
        String(8),
        nullable=False,
    )

    is_locked = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    assumptions = Column(
        String(2000),
        nullable=True,
    )

    exchange_rates = relationship(
        "ExchangeRateModel",
        back_populates="scenario",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
