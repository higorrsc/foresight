from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from src.core.infrastructure.config import GUIDType, SQLAlchemyBase


class ExchangeRateModel(SQLAlchemyBase):
    """
    SQLAlchemy model for the ExchangeRate entity.
    """

    __tablename__ = "exchange_rates"

    scenario_id = Column(
        GUIDType,
        ForeignKey("scenarios.id"),
        nullable=False,
    )

    from_currency = Column(
        String(3),
        nullable=False,
    )

    to_currency = Column(
        String(3),
        nullable=False,
    )

    rate = Column(
        Numeric(19, 7),
        nullable=False,
    )

    effective_date = Column(
        Date,
        nullable=False,
    )

    scenario = relationship(
        "ScenarioModel",
        back_populates="exchange_rates",
    )

    __table_args__ = (
        UniqueConstraint(
            "scenario_id",
            "from_currency",
            "to_currency",
            name="uq_scenario_exchange_rate",
        ),
        CheckConstraint(
            "from_currency <> to_currency",
            name="ck_different_currencies",
        ),
    )
