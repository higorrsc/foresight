from dataclasses import dataclass
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
    status: TenantStatus
    plan_id: UUID

    def _validate(self) -> None:
        """
        Validates the Tenant entity's attributes.
        """

        if not self.name or not self.name.strip():
            self.notification.add_error("Tenant name is required.")

        if len(self.name) > 100:
            self.notification.add_error("Tenant must be at most 100 characters long.")

        if not self.plan_id or not isinstance(self.plan_id, UUID):
            self.notification.add_error("Tenant plan_id must be a valid UUID.")

        if not self.status:
            self.notification.add_error("Tenant status is required.")

        if not isinstance(self.status, TenantStatus):
            self.notification.add_error("Tenant status must be a valid TenantStatus.")

        if self.notification.has_errors:
            raise EntityValidationError(self.notification.messages)
