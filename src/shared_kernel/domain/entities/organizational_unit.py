from dataclasses import dataclass, field
from uuid import UUID

from src.core.domain.entities import DescribedEntity
from src.core.domain.mixins import SoftDeletableMixin, UserAuditMixin


@dataclass(kw_only=True, eq=False, repr=False)
class OrganizationalUnit(DescribedEntity, SoftDeletableMixin, UserAuditMixin):
    """
    Entity representing an organizational unit within the system.
    """

    code: str
    parent_id: UUID | None = field(default=None, repr=False)

    def _str_fields(self) -> str:
        """
        Returns a string representation of the fields of the OrganizationalUnit entity.
        """

        return f"id={self.id}, code='{self.code}'"
