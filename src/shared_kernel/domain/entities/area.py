from dataclasses import dataclass

from src.core.domain.entities import DescribedEntity
from src.core.domain.mixins import SoftDeletableMixin, UserAuditMixin


@dataclass(kw_only=True, eq=False, repr=False)
class Area(DescribedEntity, SoftDeletableMixin, UserAuditMixin):
    """
    Entity representing a geographical or logical area within the system.
    """

    def _str_fields(self) -> str:
        """
        Returns a string representation of the fields of the Area entity.
        """

        return f"id={self.id}, description='{self.description}'"
