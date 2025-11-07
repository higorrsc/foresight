from .base import Base
from .mixins import SQLAlchemyBasicFields


class SQLAlchemyBase(Base, SQLAlchemyBasicFields):
    """
    Base class for all SQLAlchemy models.
    """

    __abstract__ = True
