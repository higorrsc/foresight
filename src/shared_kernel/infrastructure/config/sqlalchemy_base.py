from src.shared_kernel.infrastructure.config.base import Base
from src.shared_kernel.infrastructure.models._shared.mixins import SQLAlchemyBasicFields


class SQLAlchemyBase(Base, SQLAlchemyBasicFields):
    """
    Base class for all SQLAlchemy models.
    """

    __abstract__ = True
