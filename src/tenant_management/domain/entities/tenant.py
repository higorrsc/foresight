from dataclasses import dataclass, field
from uuid import UUID

from src.shared_kernel.domain._shared.entities import AbstractEntity
from src.shared_kernel.domain._shared.exceptions import EntityValidationError
from src.tenant_management.domain.value_objects import TenantStatus


@dataclass(kw_only=True, eq=False)
class Tenant(AbstractEntity):
    """
    Entity representing a Tenant in the system.
    """

    name: str
    status: TenantStatus = field(default=TenantStatus.TRIAL)
    plan_id: UUID

    def validate(self) -> None:
        """
        Validates the Tenant entity's attributes.
        """

        if not self.name or not self.name.strip():
            self.notification.add_error("Tenant name is required.")

        if self.name and len(self.name) > 100:
            self.notification.add_error("Tenant must be at most 100 characters long.")

        if not self.plan_id or not isinstance(self.plan_id, UUID):
            self.notification.add_error("Tenant plan_id must be a valid UUID.")

        if not self.status:
            self.notification.add_error("Tenant status is required.")

        if not isinstance(self.status, TenantStatus):
            self.notification.add_error("Tenant status must be a valid TenantStatus.")

        if self.notification.has_errors:
            raise EntityValidationError(self.notification.messages)

    def __str__(self) -> str:
        """
        Returns a string representation of the Tenant entity.
        """

        return f"Tenant(id={self.id}, name='{self.name}')"

    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the Tenant entity.
        """

        return f"<Tenant {self.name} ({self.id})>"
