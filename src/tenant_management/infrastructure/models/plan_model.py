from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import DECIMAL, Column, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.shared_kernel.infrastructure.config import Base, GUID_Type


class PlanModel(Base):
    """
    SQLAlchemy model for the Plan entity.
    """

    __tablename__ = "plans"

    id = Column(
        GUID_Type,
        primary_key=True,
        default=uuid4,
    )
    name = Column(
        String(100),
        nullable=False,
    )
    price: Mapped[Decimal] = mapped_column(
        DECIMAL(19, 7),
        nullable=False,
    )
    created_at = Column(
        DateTime,
        default=datetime.now,
    )
    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )
