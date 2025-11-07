from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.shared_kernel.infrastructure.config import GUID_Type, SQLAlchemyBase
from src.tenant_management.domain.value_objects import TenantStatus


class TenantModel(SQLAlchemyBase):
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
