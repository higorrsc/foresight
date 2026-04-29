from dataclasses import dataclass, field
from uuid import UUID

from src.core.domain.entities import DescribedEntity
from src.core.domain.mixins import SoftDeletableMixin, UserAuditMixin


@dataclass(kw_only=True, eq=False)
class OrganizationalUnit(DescribedEntity, SoftDeletableMixin, UserAuditMixin):
    """
    Entity representing an organizational unit within the system.
    """

    code: str
    parent_id: UUID | None = field(default=None, repr=False)

    def __str__(self) -> str:
        """
        Returns a string representation of the OrganizationalUnit entity.
        """

        return f"OrganizationalUnit(id={self.id}, code='{self.code}')"

    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the OrganizationalUnit entity.
        """

        return f"<OrganizationalUnit {self.code} ({self.id})>"
