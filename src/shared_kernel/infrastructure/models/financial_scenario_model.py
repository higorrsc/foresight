from sqlalchemy import Boolean, Column, String

from src.core.infrastructure.config import SQLAlchemyBase
from src.core.infrastructure.config.mixins import (
    SQLAlchemySoftDeletableMixin,
    SQLAlchemyTenantMixin,
    SQLAlchemyUserAuditMixin,
)


class FinancialScenarioModel(
    SQLAlchemyBase,
    SQLAlchemySoftDeletableMixin,
    SQLAlchemyTenantMixin,
    SQLAlchemyUserAuditMixin,
):
    """
    SQLAlchemy model for the FinancialScenario entity.
    """

    __tablename__ = "financial_scenarios"

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
