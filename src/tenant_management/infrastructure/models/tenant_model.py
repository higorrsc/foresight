from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.shared_kernel.infrastructure.config import Base, GUID_Type
from src.tenant_management.domain.value_objects import TenantStatus


class TenantModel(Base):
    """
    SQLAlchemy model for the Tenant entity.
    """

    __tablename__ = "tenants"

    id = Column(
        GUID_Type,
        primary_key=True,
        default=uuid4,
    )
    name = Column(
        String(100),
        nullable=False,
    )
    status: Mapped[TenantStatus] = mapped_column(
        Enum(TenantStatus),
        nullable=False,
    )
    plan_id = Column(
        GUID_Type,
        ForeignKey("plans.id"),
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
