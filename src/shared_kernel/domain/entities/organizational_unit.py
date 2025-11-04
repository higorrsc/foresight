from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from src.shared_kernel.domain._shared.entities import DescribedEntity
from src.shared_kernel.domain._shared.mixins import SoftDeletableMixin


@dataclass(kw_only=True, eq=False)
class OrganizationalUnit(DescribedEntity, SoftDeletableMixin):
    """
    Entity representing an organizational unit within the system.
    """

    code: str
    parent_id: Optional[UUID] = field(default=None, repr=False)
    tenant_id: UUID

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
