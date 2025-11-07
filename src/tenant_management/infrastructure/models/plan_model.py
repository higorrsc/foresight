from decimal import Decimal

from sqlalchemy import DECIMAL, Column, String
from sqlalchemy.orm import Mapped, mapped_column

from src.shared_kernel.infrastructure.config import (
    SQLAlchemyBase,
    SQLAlchemyUserAuditFields,
)


class PlanModel(SQLAlchemyBase, SQLAlchemyUserAuditFields):
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
