from uuid import uuid4

from sqlalchemy import Column

from .base import Base
from .custom_types import GUIDType


class SQLAlchemyBase(Base):
    """
    Base class for all SQLAlchemy models with common fields.

    Include common audit and identification fields:
        - id (UUID): Primary key.
    """

    __abstract__ = True

    id = Column(
        GUIDType,
        primary_key=True,
        default=uuid4,
    )
