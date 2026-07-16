from decimal import Decimal

from sqlalchemy import DECIMAL, Column, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.infrastructure.config import SQLAlchemyBase
from src.core.infrastructure.config.mixins import (
    SQLAlchemyUserAuditMixin,
)


class PlanModel(SQLAlchemyBase, SQLAlchemyUserAuditMixin):
    """
    SQLAlchemy model for the Plan entity.
    """

    __tablename__ = "plans"

    name = Column(
        String(100),
        nullable=False,
    )
    price: Mapped[Decimal] = mapped_column(
        DECIMAL(19, 7),
        nullable=False,
    )
