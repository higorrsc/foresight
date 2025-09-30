from uuid import uuid4

from sqlalchemy import UUID, Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from src.core.infrastructure.config.database import Base

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
    ),
    Column(
        "role_id",
        UUID(as_uuid=True),
        ForeignKey("roles.id"),
        primary_key=True,
    ),
)


class RoleModel(Base):
    """
    SQLAlchemy model for the Role entity.
    """

    __tablename__ = "roles"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    name = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )
    description = Column(String, nullable=True)

    users = relationship("UserModel", secondary=user_roles, back_populates="roles")
