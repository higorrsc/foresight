from dataclasses import dataclass

from src.core.domain.entities import DescribedEntity
from src.core.domain.mixins import SoftDeletableMixin


@dataclass(kw_only=True, eq=False)
class Area(DescribedEntity, SoftDeletableMixin):
    """
    Entity representing a geographical or logical area within the system.
    """

    def __str__(self) -> str:
        """
        Returns a string representation of the Area entity.
        """

        return f"Area(id={self.id}, description='{self.description}')"

    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the Area entity.
        """

        return f"<Area {self.description} ({self.id})>"
