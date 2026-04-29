from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.infrastructure.config import (
    GUID_Type,
    SQLAlchemyBase,
    SQLAlchemyUserAuditFields,
)
from src.tenant_management.domain.value_objects import TenantStatus


class TenantModel(SQLAlchemyBase, SQLAlchemyUserAuditFields):
    """
    SQLAlchemy model for the Tenant entity.
    """

    __tablename__ = "tenants"

    name = Column(
        String(100),
        nullable=False,
    )
    status: Mapped[TenantStatus] = mapped_column(
        Enum(TenantStatus),
        nullable=False,
        default=TenantStatus.TRIAL,
    )
    plan_id = Column(
        GUID_Type,
        ForeignKey("plans.id"),
        nullable=False,
    )
